import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter as Router } from "react-router-dom";
import App from "./App.tsx";
import { AuthProvider } from "./context/AuthContext.tsx";
import "./index.css";

const root = document.getElementById("root");

if (root)
	createRoot(root).render(
		<StrictMode>
			<Router>
				<AuthProvider>
					<App />
				</AuthProvider>
			</Router>
		</StrictMode>
	);
