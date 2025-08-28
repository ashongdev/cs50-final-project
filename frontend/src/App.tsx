import { Navigate, Route, Routes } from "react-router-dom";
import "./App.css";
import ForgotPassword from "./components/ForgotPassword";
import Home from "./pages/Home";
import Signin from "./pages/Signin";
import Signup from "./pages/Signup";

function App() {
	return (
		<Routes>
			<Route path="/" element={<Home />} />
			<Route path="/signin" element={<Signin />} />
			<Route path="/login" element={<Navigate to="/signin" />} />
			<Route path="/signup" element={<Signup />} />
			<Route path="/forgot-password" element={<ForgotPassword />} />
		</Routes>
	);
}

export default App;
