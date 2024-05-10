const express = require('express');
const cors = require('cors');
const app = express();

app.use(cors());

app.get('/api/places', async (req, res) => {
    const { lat, lng } = req.query;
    console.log(req.query);
    const apiKey = process.env.GMAP_API_KEY; 
    const url = `https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=${lat},${lng}&radius=.01&key=${apiKey}`;
    try {
        const { default: fetch } = await import('node-fetch');
        const response = await fetch(url);
        const data = await response.json();
        res.send(data);
    } catch (error) {
        console.error('Error:', error);
        res.status(500).send('Server error');
    }
});

app.listen(2000, () => console.log('Proxy server running on port 2000'));

