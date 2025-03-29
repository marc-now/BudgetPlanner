import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";
import { useState } from "react";
import api from "../api";
import "../styles/AuthenticationForm.css"
import LoadingIndicator from "./LoadingIndicator";

function AuthenticationForm()
{
    const [method, setMethod] = useState("login")
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [username, setUsername] = useState("")
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        setLoading(true);
        e.preventDefault();

        try {
            const requestData = {username, password}
            const res = await api.post("api/token/", { username, password })
            localStorage.setItem(ACCESS_TOKEN, res.data.access);
            localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
            navigate("/")

        } catch (error) {
            if (error.response && error.response.status === 401) {
                alert("Nieprawidłowa nazwa użytkownika lub hasło. Spróbuj ponownie.");
            } else {
                alert("Wystąpił błąd podczas logowania. Spróbuj ponownie później.");
            }
        } finally {
            setLoading(false)
        }
    }

    const handleRegister = async (e) => {
        setLoading(true);
        e.preventDefault();

        try {
            const requestData = {username, password}
            const res = await api.post("api/user/register/", { username, password, email })
            navigate("/login")
            alert("Account registered! You can now log in.")

        } catch (error) {
            if (error.response && error.response.status === 400) {
                alert("Podana nazwa użytkownika lub email już istnieje.");
            } else {
                alert("Wystąpił błąd podczas rejestracji. Spróbuj ponownie później.");
            }
        } finally {
            setLoading(false)
        }
    }


    return (<>
        <div className="auth-form-container">
            <div className="method-buttons-container">
                <button 
                    type="button" 
                    onClick={() => setMethod("login")} 
                    className={`form-button ${method === "login" ? "active" : ""}`}>
                    Login
                </button>
                <button 
                    type="button" 
                    onClick={() => setMethod("register")} 
                    className={`form-button ${method === "register" ? "active" : ""}`}>
                    Signup
                </button>
            </div>
            <div className="inputs-container">
                <form onSubmit={ method === "login" ? handleLogin : handleRegister} className="form-container">
                    <input
                        className="form-input"
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        placeholder="Username"
                    />
                    <input
                        className="form-input"
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Password"
                    />
                    { method === "register" && (
                        <input
                        className="form-input"
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="E-mail" />) }
                    {loading && <LoadingIndicator />}
                    <button className="form-button" type="submit">
                        {method === "login" ? "Login" : "Register"}
                    </button>
                </form>
            </div>
        </div>

    </>)
}




export default AuthenticationForm