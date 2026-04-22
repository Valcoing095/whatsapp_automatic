const { Client } = require('whatsapp-web.js');
const qrcode = require('qrcode');

const client = new Client({
    puppeteer: {
        headless: false,
        executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        args: ['--no-sandbox']
    }
});

client.on('qr', (qr) => {
    console.log('Escanea este QR con tu WhatsApp:');
    qrcode.toTerminal(qr);
});

client.on('ready', async () => {
    console.log('Cliente listo! Enviando mensaje...');
    
    const number = '573022475080';
    const message = 'Hola! Este es un mensaje automático.';
    
    const chatId = `${number}@c.us`;
    
    setTimeout(async () => {
        try {
            await client.sendMessage(chatId, message);
            console.log('Mensaje enviado exitosamente!');
        } catch (error) {
            console.log('Error al enviar mensaje:', error.message);
        }
        client.destroy();
    }, 3000);
});

client.initialize();
