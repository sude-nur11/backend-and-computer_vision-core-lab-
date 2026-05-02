const mongoose = require('mongoose');

const productSchema = new mongoose.Schema({
    name: { 
        type: String, 
        required: [true, 'Ürün adı zorunludur'],
        trim: true
    },
    price: { 
        type: Number, 
        required: [true, 'Fiyat zorunludur'],
        min: [0, 'Fiyat negatif olamaz']
    },
    category: { 
        type: String, 
        required: [true, 'Kategori zorunludur']
    },
    description: {
        type: String,
        default: ''
    },
    inStock: { 
        type: Boolean, 
        default: true 
    }
}, { timestamps: true });

module.exports = mongoose.model('Product', productSchema);
