import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";
import { useState } from "react";
import api from "../api";
//import "../styles/Form.css"
import LoadingIndicator from "./LoadingIndicator";

function RegisterForm() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [email, setEmail] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        setLoading(true);
        e.preventDefault();

        try {
            const requestData = {username, password}
            const res = await api.post("api/user/register/", { username, password, email })
            localStorage.setItem(ACCESS_TOKEN, res.data.access);
            localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
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
    };

    return (
        <form onSubmit={handleSubmit} className="form-container">
            <h1>Register</h1>
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
            <input
                className="form-input"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="E-mail"
            />
            {loading && <LoadingIndicator />}
            <button className="form-button" type="submit">
                Register
            </button>
        </form>
    );
}

export default RegisterForm