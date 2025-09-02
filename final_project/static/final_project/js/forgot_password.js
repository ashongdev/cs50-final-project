document.addEventListener("DOMContentLoaded", () => {
	const requestBtn = document.querySelector(".request-new");

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

	requestBtn.addEventListener("click", () => {
		fetch("/request_code", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFToken": getCookie("csrftoken"),
			},

			credentials: "include",
		}).then((response) => {
			response.json().then((result) => {
				alert(result.message);
			});
		});
	});
});
