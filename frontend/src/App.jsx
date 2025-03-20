import React from "react"
import { BrowserRouter, Routes, Route, Navigate} from "react-router-dom"
import Auth from "./pages/Auth"
import Home from "./pages/Home"
import NotFound from "./pages/NotFound"
import ProtectedRoute from "./components/ProtectedRoute"

function Logout() {
  console.log("logout")
  localStorage.clear()
  return <Navigate to="/login" />
}

function RegisterAndLogout() {
  localStorage.clear()
  return <Navigate to="/login" />
}

function App() {
  return (<>
    <BrowserRouter>
    { 
    // <Navbar /> 
    }
      <Routes>
        <Route 
          path="/"
          element={
            <ProtectedRoute>
              <Home />
            </ProtectedRoute>
          }
        />
        <Route 
          path="/login"
          element={
            <Auth/>
          }
        />
        <Route 
          path="/logout"
          element={
            <Logout />
          }
        />
        <Route 
          path="/register"
          element={
            <RegisterAndLogout />
          }
        />
        <Route 
          path="*"
          element={
            <NotFound />
          }
        />
      </Routes>
    </BrowserRouter>
  </>)
}

export default App
