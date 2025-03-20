
import { useState } from "react";
import "../styles/Auth.css"
import AuthenticationForm from "../components/AuthenticationForm";
import { TileSlider, Tile } from "../components/TileSlider";

function Auth() {
    const [isLogin, setIsLogin] = useState(true)

    return (<>
    <div className="auth-page-root">
        <div className="container">
            <section className="left-section">
                <h3>BudgetPlanner</h3>               
                <AuthenticationForm />
            </section>
            <section className="right-section">
                <TileSlider>
                    <Tile><p style={{fontSize: "80px"}}>Plan you budget.</p></Tile>
                    <Tile><p style={{fontSize: "80px"}}>Manage your finances.</p></Tile>
                    <Tile><p style={{fontSize: "80px"}}>Save your money.</p></Tile>
                </TileSlider>
            </section>
        </div>
        <footer className="footer">
            by Marcin Nowakowski
        </footer>
    </div>

    </>)
}

export default Auth

