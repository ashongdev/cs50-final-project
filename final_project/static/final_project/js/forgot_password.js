document.addEventListener("DOMContentLoaded", () => {
	function getCookie(name) {
		let cookieValue = null;
		if (document.cookie && document.cookie !== "") {
			const cookies = document.cookie.split(";");
			for (let i = 0; i < cookies.length; i++) {
				const cookie = cookies[i].trim();
				// Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) === name + "=") {
					cookieValue = decodeURIComponent(
						cookie.substring(name.length + 1)
					);
					break;
				}
			}
		}
		return cookieValue;
	}
	const codeForm = document.querySelector(".code-form");
	const statusEl = document.querySelector(".status-msg"); // permanent element
	const requestBtn = document.querySelector(".request-new");

	codeForm &&
		codeForm.addEventListener("submit", (e) => {
			e.preventDefault();

			const email = document.getElementById("email").value;
			const code = document.getElementById("code");

			fetch("/code", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
					"X-CSRFToken": getCookie("csrftoken"),
				},
				credentials: "include",
				body: JSON.stringify({ email, code: code.value }),
			}).then((response) => {
				response.json().then((result) => {
					if (result.status === 410 || result.status == 400) {
						// Error states
						statusEl.textContent = result.message;
						statusEl.classList.remove("success");
						statusEl.classList.add("error");

						code.classList.add("code-error");
						document
							.getElementById("verification-label")
							.classList.add("verification-label");

						// Only show request button when code is expired
						if (result.status === 410) {
							requestBtn.style.opacity = 1;
						} else {
							requestBtn.style.opacity = 0;
						}
					} else if (response.status === 200) {
						window.location.href = `/set_new_password?email=${result.email}`;
					}
				});
			});
		});

	requestBtn &&
		requestBtn.addEventListener("click", () => {
			const urlParams = new URLSearchParams(window.location.search);
			const email = urlParams.get("email");

			fetch("/request_code", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
					"X-CSRFToken": getCookie("csrftoken"),
				},
				body: JSON.stringify({ email }),
				credentials: "include",
			}).then((response) => {
				response.json().then((result) => {
					requestBtn.style.opacity = 0;

					statusEl.textContent = result.message;
					statusEl.classList.remove("error");
					statusEl.classList.add("success");
				});
			});
		});

	const forgotForm = document.querySelector(".forgot-form");
	forgotForm &&
		forgotForm.addEventListener("submit", (e) => {
			e.preventDefault();

			const email = document.getElementById("email")?.value;
			fetch("/forgot_password", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
					"X-CSRFToken": getCookie("csrftoken"),
				},
				credentials: "include",
				body: JSON.stringify({ email }),
			}).then((response) => {
				response.json().then((result) => {
					if (result.status === 400) {
						document.querySelector(".error").innerHTML =
							result.message;
					} else {
						window.location.href = `/code?email=${result.email}`;
					}
				});
			});
		});

	const setNewwPasswordForm = document.querySelector(
		".set-new-password-form"
	);
	setNewwPasswordForm &&
		setNewwPasswordForm.addEventListener("submit", (e) => {
			e.preventDefault();

			const email = document.getElementById("email")?.value;
			const password = document.getElementById("password")?.value;
			const confirmation = document.getElementById("confirmation")?.value;

			fetch("/set_new_password", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
					"X-CSRFToken": getCookie("csrftoken"),
				},
				credentials: "include",
				body: JSON.stringify({ email, password, confirmation }),
			}).then((response) => {
				response.json().then((result) => {
					if (result.status === 400) {
						document.querySelector(".error").innerHTML =
							result.message;
					} else {
						window.location.href = `/notes`;
					}
				});
			});
		});
});
