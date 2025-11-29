import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Landing } from './pages/Landing';
import { Dashboard } from './pages/Dashboard';
import { AgentsPage } from './pages/Agents';
import { Agent1 } from './pages/Agent1';
import { Agent2 } from './pages/Agent2';
import { Agent3 } from './pages/Agent3';
import { Agent4 } from './pages/Agent4';
import { Agent5 } from './pages/Agent5';
import { Agent6 } from './pages/Agent6';
import { Agent7 } from './pages/Agent7';
import { Agent8 } from './pages/Agent8';
import { Agent9 } from './pages/Agent9';
import { Agent10 } from './pages/Agent10';
import { Agent11 } from './pages/Agent11';
import { Agent12 } from './pages/Agent12';

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Landing />} />
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/agents" element={<AgentsPage />} />
                <Route path="/agent/1" element={<Agent1 />} />
                <Route path="/agent/2" element={<Agent2 />} />
                <Route path="/agent/3" element={<Agent3 />} />
                <Route path="/agent/4" element={<Agent4 />} />
                <Route path="/agent/5" element={<Agent5 />} />
                <Route path="/agent/6" element={<Agent6 />} />
                <Route path="/agent/7" element={<Agent7 />} />
                <Route path="/agent/8" element={<Agent8 />} />
                <Route path="/agent/9" element={<Agent9 />} />
                <Route path="/agent/10" element={<Agent10 />} />
                <Route path="/agent/11" element={<Agent11 />} />
                <Route path="/agent/12" element={<Agent12 />} />
            </Routes>
        </Router>
    );
}

export default App;
