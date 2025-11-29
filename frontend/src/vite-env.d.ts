/// <reference types="vite/client" />

interface ImportMetaEnv {
    readonly VITE_API_URL?: string
    readonly VITE_CARDANO_NETWORK?: string
    readonly VITE_BLOCKFROST_PROJECT_ID?: string
}

interface ImportMeta {
    readonly env: ImportMetaEnv
}
