import { Link } from "react-router-dom";
import { LogOut } from "lucide-react";
import "../styles/Navbar.css";

function Navbar() {
    return (
        <nav className="navbar">
            {/* Logo po lewej */}
            <div className="logo">
                <Link to="/">BudgetPlanner</Link>
            </div>
            
            {/* Linki na środku */}
            <div className="nav-links">
                <Link to="/" className="nav-link">PULPIT</Link>
                <span className="nav-placeholder">HISTORIA</span>
                <span className="nav-placeholder">PROFIL</span>
            </div>
            
            {/* Przyciski po prawej */}
            <div className="nav-buttons">
                {/* Zmiana języka (PL) */}
                <div className="language-switcher">
                    <div className="language-icon"></div>
                    <span>PL</span>
                </div>
                
                {/* Logout */}
                <Link to="/logout" className="logout-button">
                    <LogOut size={24} />
                </Link>
            </div>
        </nav>
    );
}

export default Navbar