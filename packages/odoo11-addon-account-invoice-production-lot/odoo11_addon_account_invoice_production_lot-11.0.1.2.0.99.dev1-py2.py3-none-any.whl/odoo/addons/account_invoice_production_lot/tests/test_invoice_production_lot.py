# Copyright 2011 Domsense s.r.l. <http://www.domsense.com>
# Copyright 2013 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
# Copyright 2017 Vicent Cubells <vicent.cubells@tecnativa.com>
# Copyright 2018 Alex Comba <alex.comba@agilebg.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestProdLot(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestProdLot, cls).setUpClass()
        cls.partner = cls.env['res.partner'].create({
            'name': 'Test partner',
            'lang': 'en_US',
        })
        cls.product = cls.env['product.product'].create({
            'name': 'Product Test',
            'type': 'product',
            'tracking': 'lot',
            'invoice_policy': 'delivery',
        })
        cls.product2 = cls.env['product.product'].create({
            'name': 'Product Test 2',
            'type': 'product',
            'tracking': 'serial',
            'invoice_policy': 'delivery',
        })
        cls.sale = cls.env['sale.order'].create({
            'partner_id': cls.partner.id,
            'partner_invoice_id': cls.partner.id,
            'partner_shipping_id': cls.partner.id,
            'order_line': [
                (0, 0, {
                    'name': cls.product.name,
                    'product_id': cls.product.id,
                    'product_uom_qty': 4,
                    'product_uom': cls.product.uom_id.id,
                    'price_unit': 15.0,
                }),
                (0, 0, {
                    'name': cls.product2.name,
                    'product_id': cls.product2.id,
                    'product_uom_qty': 1,
                    'product_uom': cls.product2.uom_id.id,
                    'price_unit': 10.0,
                }),
            ],
        })
        cls.lot1 = cls.env['stock.production.lot'].create({
            'name': 'Lot 1',
            'product_id': cls.product.id,
        })
        cls.lot2 = cls.env['stock.production.lot'].create({
            'name': 'Lot 2',
            'product_id': cls.product.id,
        })
        cls.serial = cls.env['stock.production.lot'].create({
            'name': 'Serial 1',
            'product_id': cls.product2.id,
        })
        cls.stock_location = cls.env.ref('stock.stock_location_stock')
        cls.customer_location = cls.env.ref('stock.stock_location_customers')
        cls.picking_type_out = cls.env.ref('stock.picking_type_out')

    def qty_on_hand(self, product, location, quantity, lot):
        """Update Product quantity."""
        wiz = self.env['stock.change.product.qty'].create({
            'location_id': location.id,
            'product_id': product.id,
            'new_quantity': quantity,
            'lot_id': lot.id,
        })
        wiz.change_product_qty()

    def test_00_sale_stock_invoice_product_lot(self):
        # update quantities with their related lots
        self.qty_on_hand(self.product, self.stock_location, 2, self.lot1)
        self.qty_on_hand(self.product, self.stock_location, 2, self.lot2)
        self.qty_on_hand(self.product2, self.stock_location, 1, self.serial)
        # confirm quotation
        self.sale.action_confirm()
        picking = self.sale.picking_ids[:1]
        picking.action_confirm()
        picking.action_assign()
        for sml in picking.move_lines.mapped('move_line_ids'):
            sml.qty_done = sml.product_qty
        picking.action_done()
        # create invoice
        inv_id = self.sale.action_invoice_create()
        invoice = self.env['account.invoice'].browse(inv_id)
        self.assertEqual(len(invoice.invoice_line_ids), 2)
        line = invoice.invoice_line_ids.filtered(
            lambda x: x.product_id == self.product
        )
        # We must have two lots
        self.assertEqual(len(line.prod_lot_ids.ids), 2)
        self.assertIn('Lot 1', line.lot_formatted_note)
        self.assertIn('Lot 2', line.lot_formatted_note)
        # check if quantity is displayed in lot_formatted_note
        self.assertIn("(2.0)", line.lot_formatted_note)
        # Check S/N
        line2 = invoice.invoice_line_ids - line
        self.assertIn("S/N", line2.lot_formatted_note)
        self.assertIn("Serial 1", line2.lot_formatted_note)

    def test_01_sale_stock_delivery_partial_invoice_product_lot(self):
        # update quantities with their related lots
        self.qty_on_hand(self.product, self.stock_location, 3, self.lot1)
        self.qty_on_hand(self.product, self.stock_location, 3, self.lot2)
        # confirm quotation
        self.sale.action_confirm()
        picking = self.sale.picking_ids[:1]
        picking.action_confirm()
        picking.action_assign()
        # deliver partially only one lot
        picking.move_lines[0].move_line_ids[0].write({'qty_done': 2.0})
        backorder_wiz_id = picking.button_validate()['res_id']
        backorder_wiz = self.env['stock.backorder.confirmation'].browse(
            backorder_wiz_id)
        backorder_wiz.process()
        # create invoice
        inv_id = self.sale.action_invoice_create()
        invoice = self.env['account.invoice'].browse(inv_id)
        self.assertEqual(len(invoice.invoice_line_ids), 1)
        line = invoice.invoice_line_ids
        # We must have only one lot
        self.assertEqual(len(line.prod_lot_ids.ids), 1)
        self.assertEqual(line.prod_lot_ids.id, self.lot1.id)
        self.assertIn('Lot 1', line.lot_formatted_note)
        self.assertNotIn('Lot 2', line.lot_formatted_note)
        # check if quantity is displayed in lot_formatted_note
        self.assertIn("(2.0)", line.lot_formatted_note)

    def test_02_sale_stock_delivery_partial_invoice_product_lot(self):
        # update quantities with their related lots
        self.qty_on_hand(self.product, self.stock_location, 3, self.lot1)
        self.qty_on_hand(self.product, self.stock_location, 3, self.lot2)
        # confirm quotation
        self.sale.action_confirm()
        picking = self.sale.picking_ids[:1]
        picking.action_confirm()
        picking.action_assign()
        # deliver partially both lots
        picking.move_lines[0].move_line_ids[0].write({'qty_done': 1.0})
        picking.move_lines[0].move_line_ids[1].write({'qty_done': 1.0})
        backorder_wiz_id = picking.button_validate()['res_id']
        backorder_wiz = self.env['stock.backorder.confirmation'].browse(
            [backorder_wiz_id])
        backorder_wiz.process()
        # create invoice
        inv_id = self.sale.action_invoice_create()
        invoice = self.env['account.invoice'].browse(inv_id)
        self.assertEqual(len(invoice.invoice_line_ids), 1)
        line = invoice.invoice_line_ids
        # We must have two lots
        self.assertEqual(len(line.prod_lot_ids.ids), 2)
        self.assertIn(self.lot1.id, line.prod_lot_ids.ids)
        self.assertIn(self.lot2.id, line.prod_lot_ids.ids)
        self.assertIn('Lot 1', line.lot_formatted_note)
        self.assertIn('Lot 2', line.lot_formatted_note)
        # check if both quantities are displayed in lot_formatted_note
        self.assertIn("(1.0)", line.lot_formatted_note)
        self.assertNotIn("(2.0)", line.lot_formatted_note)
