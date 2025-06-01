const http = require('http');
const fs = require('fs');
const path = require('path');

// Read data from file
function readData() {
    try {
        const data = fs.readFileSync('data.json', 'utf8');
        return JSON.parse(data);
    } catch (error) {
        return {
            testResults: [],
            homeroomTeachers: [],
            classStudents: {},
            studentCodes: {}
        };
    }
}

// Write data to file
function writeData(data) {
    fs.writeFileSync('data.json', JSON.stringify(data, null, 2));
}

const server = http.createServer((req, res) => {
    // Set CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    // Handle preflight requests
    if (req.method === 'OPTIONS') {
        res.writeHead(204);
        res.end();
        return;
    }

    // Handle API endpoints
    if (req.url.startsWith('/api/')) {
        const data = readData();
        
        if (req.method === 'GET') {
            if (req.url === '/api/data') {
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify(data));
                return;
            }
        } else if (req.method === 'POST') {
            let body = '';
            req.on('data', chunk => {
                body += chunk.toString();
            });
            
            req.on('end', () => {
                try {
                    const newData = JSON.parse(body);
                    writeData(newData);
                    res.writeHead(200, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ success: true }));
                } catch (error) {
                    res.writeHead(400, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ error: 'Invalid data' }));
                }
            });
            return;
        }
    }

    // Serve static files
    let filePath = '.' + req.url;
    if (filePath === './') {
        filePath = './check-score.html';
    }

    const extname = path.extname(filePath);
    let contentType = 'text/html';
    
    switch (extname) {
        case '.js':
            contentType = 'text/javascript';
            break;
        case '.css':
            contentType = 'text/css';
            break;
    }

    fs.readFile(filePath, (error, content) => {
        if (error) {
            if(error.code === 'ENOENT') {
                res.writeHead(404);
                res.end('File not found');
            } else {
                res.writeHead(500);
                res.end('Server Error: '+error.code);
            }
        } else {
            res.writeHead(200, { 'Content-Type': contentType });
            res.end(content, 'utf-8');
        }
    });
});

const PORT = 3000;
server.listen(PORT, () => {
    const os = require('os');
    const networkInterfaces = os.networkInterfaces();
    let ipAddress = '';

    // Find the first non-internal IPv4 address
    Object.keys(networkInterfaces).forEach((interfaceName) => {
        networkInterfaces[interfaceName].forEach((interface) => {
            if (interface.family === 'IPv4' && !interface.internal) {
                ipAddress = interface.address;
            }
        });
    });

    console.log(`Server running at:`);
    console.log(`- Local:   http://localhost:${PORT}`);
    console.log(`- Network: http://${ipAddress}:${PORT}`);
}); 