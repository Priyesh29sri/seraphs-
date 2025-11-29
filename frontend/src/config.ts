export const API_URL = import.meta.env.VITE_API_URL ||
    (import.meta.env.PROD
        ? 'https://seraphs-production.up.railway.app'
        : 'http://localhost:8000');

export const CARDANO_NETWORK = import.meta.env.VITE_CARDANO_NETWORK || 'mainnet';
export const BLOCKFROST_PROJECT_ID = import.meta.env.VITE_BLOCKFROST_PROJECT_ID || '';
