import { ReactNode } from 'react';
import { Navbar } from './Navbar';
import { Sidebar } from './Sidebar';

interface LayoutProps {
    children: ReactNode;
}

export const Layout = ({ children }: LayoutProps) => {
    return (
        <div className="min-h-screen bg-dark-bg">
            <Navbar />
            <Sidebar />

            <main className="ml-64 mt-[73px] p-8 min-h-[calc(100vh-73px)]">
                <div className="container mx-auto">
                    {children}
                </div>
            </main>
        </div>
    );
};
