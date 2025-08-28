import gitHubIcon from "../assets/github-icon-1-logo.svg";
import googleIcon from "../assets/google-icon-logo-svgrepo-com.svg";

const ThirdPartyAuth = ({ auth }: { auth: "Sign up" | "Sign in" }) => {
	const btnClick = async () => {
		try {
			window.location.href =
				"http://127.0.0.1:8000/accounts/google/login/?process=login&next=http://127.0.0.1:5173/";
		} catch (error) {
			console.log("🚀 ~ btnClick ~ error:", error);
		}
	};
	return (
		<>
			<div className="flex justify-center-items-center gap-5 mt-10">
				<button className="auth-btn" onClick={btnClick}>
					<img src={googleIcon} alt="" className="icon" />
					<span>{auth} with Google</span>
				</button>

				<button className="auth-btn">
					<img
						src={gitHubIcon}
						alt=""
						className="w-[18px] h-[18px]"
					/>
					<span>{auth} with GitHub</span>
				</button>
			</div>
		</>
	);
};

export default ThirdPartyAuth;
