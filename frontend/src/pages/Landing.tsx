import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { lazy, Suspense } from 'react';
import { ButtonColorful } from '../components/ui/button-colorful';
import { Card } from '../components/ui/card';

const SplineScene = lazy(() => import('../components/ui/splite').then(module => ({ default: module.SplineScene })));

const ROBOT_SCENE_URL = "https://prod.spline.design/kZDDjO5HuC9GJUM2/scene.splinecode";

export const Landing = () => {
    const navigate = useNavigate();

    return (
        <div className="w-screen h-screen bg-black overflow-hidden">
            <Card className="w-full h-full bg-black/[0.96] relative overflow-hidden border-0 rounded-none">
                {/* Spotlight Effect */}
                <div className="absolute -top-40 left-0 md:left-60 md:-top-20 pointer-events-none">
                    <svg
                        className="animate-spotlight pointer-events-none absolute z-[1] h-[169%] w-[138%] lg:w-[84%] opacity-0"
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 3787 2842"
                        fill="none"
                    >
                        <g filter="url(#filter)">
                            <ellipse
                                cx="1924.71"
                                cy="273.501"
                                rx="1924.71"
                                ry="273.501"
                                transform="matrix(-0.822377 -0.568943 -0.568943 0.822377 3631.88 2291.09)"
                                fill="white"
                                fillOpacity="0.21"
                            />
                        </g>
                        <defs>
                            <filter
                                id="filter"
                                x="0.860352"
                                y="0.838989"
                                width="3785.16"
                                height="2840.26"
                                filterUnits="userSpaceOnUse"
                                colorInterpolationFilters="sRGB"
                            >
                                <feFlood floodOpacity="0" result="BackgroundImageFix" />
                                <feBlend
                                    mode="normal"
                                    in="SourceGraphic"
                                    in2="BackgroundImageFix"
                                    result="shape"
                                />
                                <feGaussianBlur
                                    stdDeviation="151"
                                    result="effect1_foregroundBlur_1065_8"
                                />
                            </filter>
                        </defs>
                    </svg>
                </div>

                <div className="flex h-full">
                    {/* Left content - Text and Button */}
                    <div className="flex-1 p-8 md:p-16 relative z-10 flex flex-col justify-center">
                        <motion.div
                            initial={{ opacity: 0, x: -50 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ duration: 1, delay: 0.3 }}
                        >
                            <h1 className="text-7xl md:text-8xl lg:text-9xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 mb-8 tracking-tight leading-none">
                                SERAPHS
                            </h1>
                            <p className="mt-6 text-gray-300 text-2xl md:text-3xl font-light max-w-2xl leading-relaxed tracking-wide">
                                Multi-Agent Compliance Intelligence
                            </p>
                            <p className="mt-4 text-gray-400 text-lg md:text-xl font-light max-w-2xl leading-relaxed">
                                Harness the power of 12 specialized AI agents working in perfect harmony.
                                Experience unprecedented accuracy, transparency, and intelligence in regulatory compliance.
                            </p>
                            <motion.div
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ duration: 0.6, delay: 0.8 }}
                                className="mt-12"
                            >
                                <ButtonColorful
                                    label="Enter Dashboard"
                                    onClick={() => navigate('/dashboard')}
                                    className="text-xl px-12 py-6 h-auto"
                                />
                            </motion.div>
                            <motion.p
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                transition={{ duration: 1, delay: 1.2 }}
                                className="text-gray-500 mt-8 text-sm font-light tracking-wider uppercase"
                            >
                                Powered by 115+ Tools
                            </motion.p>
                        </motion.div>
                    </div>

                    {/* Right content - 3D Robot */}
                    <motion.div
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ duration: 1, delay: 0.5 }}
                        className="flex-1 relative"
                    >
                        <Suspense fallback={
                            <div className="w-full h-full flex items-center justify-center">
                                <div className="text-center">
                                    <div className="text-9xl mb-4 animate-pulse">🤖</div>
                                    <p className="text-gray-400 text-xl">Loading...</p>
                                </div>
                            </div>
                        }>
                            <SplineScene
                                scene={ROBOT_SCENE_URL}
                                className="w-full h-full"
                            />
                        </Suspense>
                    </motion.div>
                </div>
            </Card>
        </div>
    );
};
