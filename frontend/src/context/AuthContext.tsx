// AuthContext.js
import axios from "axios";
import {
	createContext,
	Dispatch,
	ReactNode,
	SetStateAction,
	useContext,
	useEffect,
	useState,
} from "react";

type AuthContextType = {
	user: any;
	setUser: Dispatch<SetStateAction<null>>;
	loading: boolean;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
	const [user, setUser] = useState(null);
	const [loading, setLoading] = useState(true);

	const api = axios.create({
		baseURL: "http://127.0.0.1:8000",
		withCredentials: true,
	});
	async function getCurrentUser() {
		try {
			// Use this instance for all authenticated requests
			const res = await api.get("/check_user");

			if (res.data.ok) {
				const data = res.data;
				setUser(data);
			} else {
				setUser(null);
			}
		} catch (err) {
			console.error("Auth check failed", err);
			setUser(null);
		} finally {
			setLoading(false);
		}
	}
	useEffect(() => {
		getCurrentUser();
	}, []);

	return (
		<AuthContext.Provider value={{ user, setUser, loading }}>
			{children}
		</AuthContext.Provider>
	);
}

export function useAuth() {
	return useContext(AuthContext);
}
