const express = require('express');
const router = express.Router();
const upload = require('../middleware/uploadMiddleware');
const Product = require('../models/Product');

// Yeni ürün ekleme (Görsel ile birlikte)
router.post('/add', upload.single('image'), async (req, res) => {
    try {
        const { name, price, category, description } = req.body;
        const imageUrl = req.file ? `/uploads/${req.file.filename}` : '';

        const newProduct = new Product({
            name,
            price,
            category,
            description,
            imageUrl // Modelde bu alanın olduğundan emin olmalıyız
        });

        await newProduct.save();
        res.status(201).json({ success: true, data: newProduct });
    } catch (error) {
        res.status(400).json({ success: false, error: error.message });
    }
});

module.exports = router;
