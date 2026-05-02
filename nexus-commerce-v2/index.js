require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const authRoutes = require('./routes/authRoutes');

const app = express();
app.use(express.json());

// Veritabanı Bağlantısı
mongoose.connect(process.env.MONGODB_URI)
    .then(() => console.log('Nexus V2: MongoDB Bağlantısı Başarılı'))
    .catch(err => console.log('Bağlantı Hatası:', err));

// Rotalar
app.use('/api/auth', authRoutes);

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Sunucu ${PORT} portunda yayında`));
