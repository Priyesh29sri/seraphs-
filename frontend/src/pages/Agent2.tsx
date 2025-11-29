import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Shield, ArrowLeft, CheckCircle, AlertTriangle, Lock, FileCheck } from 'lucide-react';
import { Card } from '../components/ui/card';

export const Agent2 = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <div className="bg-gray-800 border-b border-gray-700">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <motion.button
            onClick={() => navigate('/dashboard')}
            className="mb-6 flex items-center gap-2 text-gray-400 hover:text-white transition-colors"
            whileHover={{ x: -5 }}
          >
            <ArrowLeft className="w-5 h-5" />
            Back to Dashboard
          </motion.button>

          <div className="flex items-center gap-6">
            <div className="p-4 bg-purple-600/20 rounded-2xl">
              <Shield className="w-12 h-12 text-purple-400" />
            </div>
            <div>
              <h1 className="text-4xl font-bold mb-2">Agent 2: Authenticity Oracle</h1>
              <p className="text-gray-400 text-lg">Cryptographic Document Verification</p>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-6 py-16">
        {/* Global Novelty Banner */}
        <div className="mb-12 p-8 bg-gradient-to-r from-purple-900/30 to-pink-900/30 border border-purple-500/30 rounded-2xl">
          <h2 className="text-2xl font-bold mb-4 text-purple-400">🌍 Global Novelty</h2>
          <p className="text-gray-300 text-lg leading-relaxed mb-4">
            World's first <span className="font-bold text-purple-400">cryptographic authenticity verification system</span> combining
            TLS fingerprinting, digital signatures, and tamper detection for regulatory documents.
          </p>
          <div className="bg-purple-500/10 border-l-4 border-purple-500 p-4 rounded">
            <p className="text-sm text-purple-300 font-semibold">
              💡 Why It Matters: Prevents document tampering and ensures regulatory content integrity,
              providing cryptographic proof of authenticity for audit trails.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          {/* Left Column - Info */}
          <div>
            <h2 className="text-3xl font-bold mb-6">Overview</h2>
            <p className="text-gray-300 text-lg leading-relaxed mb-8">
              Agent 2 verifies the authenticity of every ingested document using cryptographic techniques.
              It validates TLS certificates, checks digital signatures, and detects any tampering attempts.
            </p>

            <h3 className="text-2xl font-bold mb-4">Key Features</h3>
            <ul className="space-y-3 text-gray-300">
              <li className="flex items-start gap-3">
                <div className="w-2 h-2 bg-purple-500 rounded-full mt-2" />
                <span><strong>TLS Certificate Validation:</strong> Verifies SSL/TLS certificates and chains</span>
              </li>
              <li className="flex items-start gap-3">
                <div className="w-2 h-2 bg-purple-500 rounded-full mt-2" />
                <span><strong>Digital Signature Verification:</strong> Validates PDF signatures and metadata</span>
              </li>
              <li className="flex items-start gap-3">
                <div className="w-2 h-2 bg-purple-500 rounded-full mt-2" />
                <span><strong>Tamper Detection:</strong> Hash comparison to detect modifications</span>
              </li>
              <li className="flex items-start gap-3">
                <div className="w-2 h-2 bg-purple-500 rounded-full mt-2" />
                <span><strong>Source Authenticity Scoring:</strong> Confidence metrics for document origin</span>
              </li>
              <li className="flex items-start gap-3">
                <div className="w-2 h-2 bg-purple-500 rounded-full mt-2" />
                <span><strong>Chain-of-Custody:</strong> Tracks document lineage and modifications</span>
              </li>
            </ul>
          </div>

          {/* Right Column - Stats */}
          <div className="space-y-6">
            <Card className="bg-gray-800/50 border-gray-700 p-6">
              <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <CheckCircle className="w-5 h-5 text-green-500" />
                Verification Stats
              </h3>
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-gray-400">Documents Verified</span>
                    <span className="font-bold">1,247</span>
                  </div>
                  <div className="w-full bg-gray-700 rounded-full h-2">
                    <div className="bg-purple-500 h-2 rounded-full" style={{ width: '95%' }} />
                  </div>
                </div>
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-gray-400">Authenticity Score</span>
                    <span className="font-bold text-green-400">98.5%</span>
                  </div>
                  <div className="w-full bg-gray-700 rounded-full h-2">
                    <div className="bg-green-500 h-2 rounded-full" style={{ width: '98.5%' }} />
                  </div>
                </div>
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-gray-400">Tamper Attempts Detected</span>
                    <span className="font-bold text-red-400">3</span>
                  </div>
                </div>
              </div>
            </Card>

            <Card className="bg-gray-800/50 border-gray-700 p-6">
              <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <Lock className="w-5 h-5 text-purple-500" />
                Security Features
              </h3>
              <div className="space-y-3 text-sm text-gray-300">
                <div className="flex items-center gap-2">
                  <FileCheck className="w-4 h-4 text-green-500" />
                  <span>X.509 Certificate Validation</span>
                </div>
                <div className="flex items-center gap-2">
                  <FileCheck className="w-4 h-4 text-green-500" />
                  <span>OCSP Revocation Checking</span>
                </div>
                <div className="flex items-center gap-2">
                  <FileCheck className="w-4 h-4 text-green-500" />
                  <span>PDF/A Signature Verification</span>
                </div>
                <div className="flex items-center gap-2">
                  <FileCheck className="w-4 h-4 text-green-500" />
                  <span>SHA-256 Integrity Checks</span>
                </div>
              </div>
            </Card>
          </div>
        </div>

        {/* Status Section */}
        <div className="mt-16 text-center">
          <div className="inline-flex items-center gap-3 bg-green-900/20 border border-green-500/30 px-8 py-4 rounded-full">
            <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse" />
            <span className="text-green-400 font-semibold text-lg">Agent 2: Operational & Verifying</span>
          </div>
        </div>
      </div>
    </div>
  );
};
