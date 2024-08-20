const dotenv = require('dotenv');
const path = require('path');

// Load .env file
dotenv.config({ path: path.resolve(__dirname, '.env') });

// Load .env.local file if it exists
const localEnvPath = path.resolve(__dirname, '.env.local');
if (require('fs').existsSync(localEnvPath)) {
  dotenv.config({ path: localEnvPath });
}
