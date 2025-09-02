document.addEventListener("DOMContentLoaded", function () {
	// Use buttons to toggle between views
	document
		.querySelector("#inbox")
		.addEventListener("click", () => load_mailbox("inbox"));
	document
		.querySelector("#sent")
		.addEventListener("click", () => load_mailbox("sent"));
	document
		.querySelector("#archived")
		.addEventListener("click", () => load_mailbox("archive"));
	document.querySelector("#compose").addEventListener("click", compose_email);
	document.querySelector("#compose-form").addEventListener("submit", (e) => {
		e.preventDefault();

		submitForm();
	});

	// By default, load the inbox
	load_mailbox("inbox");
});

function submitForm() {
	const recipients = document.querySelector("#compose-recipients").value;
	const subject = document.querySelector("#compose-subject").value;
	const body = document.querySelector("#compose-body").value;

	fetch("/mail/emails", {
		method: "POST",
		credentials:"include",
		body: JSON.stringify({ recipients, subject, body }),
	})
		.then((response) => response.json())
		.then((data) => {
			if (!data?.error) {
				alert(data.message);

				load_mailbox("sent");
			} else {
				alert(data.error);
			}
		})
		.catch((error) => {
			alert(error);
		});
}

function compose_email() {
	// Show compose view and hide other
	const emailsView = document.querySelector("#emails-view");
	const emailView = document.querySelector("#email-view");
	const composeView = document.querySelector("#compose-view");

	emailsView.style.display = "none";
	emailView.style.display = "none";
	composeView.style.display = "block";

	// Clear out composition fields
	document.querySelector("#compose-recipients").value = "";
	document.querySelector("#compose-subject").value = "";
	document.querySelector("#compose-body").value = "";
}

function load_mailbox(mailbox) {
	// Show the mailbox and hide other views
	const emailsView = document.querySelector("#emails-view");
	const composeView = document.querySelector("#compose-view");
	const emailView = document.querySelector("#email-view");

	emailsView.style.display = "block";
	composeView.style.display = "none";
	emailView.style.display = "none";

	// Show the mailbox name
	emailsView.innerHTML = `<h3>${
		mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
	}</h3>`;

	fetch(`/mail/emails/${mailbox}`, {
		method: "GET",
		credentials:"include",
	})
		.then((response) => response.json())
		.then((result) => {
			result.forEach((mail) => {
				const divElement = document.createElement("div");
				divElement.classList.add("email-card");
				divElement.classList.add(mail.read ? "read" : "unread");
				divElement.innerHTML = `
               <p>${mail.subject}</p>
               <p>${mail.sender}</p>
               <p>${mail.timestamp}</p>
            `;
				divElement.addEventListener("click", () => {
					viewEmail(mail.id, mailbox);
				});

				emailsView.appendChild(divElement);
			});
		});
}

function viewEmail(id, mailbox) {
	const emailView = document.querySelector("#email-view");
	const emailsView = document.querySelector("#emails-view");
	emailView.style.display = "block";
	emailsView.style.display = "none";

	// Get emails
	fetch(`/mail/emails/${id}`, {
		method: "GET",
		credentials:"include",
	})
		.then((response) => response.json())
		.then((result) => {
			// Mark email as read
			emailView.innerHTML = `
               <div class="full-email">
                  <div class="email-header">
                     <p><strong>From:</strong> ${result.sender}</p>
                     <p><strong>To:</strong> ${result.recipients}</p>
                     <p><strong>Subject:</strong> ${
							result.subject ? result.subject : "(No subject)"
						}</p>
                     <p><strong>Timestamp:</strong> ${result.timestamp}</p>
                  </div>
                  <hr />
                  <div class="email-body">
                     <p>${result.body ? result.body : "(No content)"}</p>
                  </div>
               </div>`;

				const buttonElem = document.createElement("button");
				const buttonElem1 = document.createElement("button");
				buttonElem1.innerText = "Reply";
				buttonElem.innerText = result.archived
					? "Unarchive"
					: "Archive";

				mailbox !== "sent" && emailView.appendChild(buttonElem);
				emailView.appendChild(buttonElem1);

				const archiveValue = result.archived ? false : true;
				buttonElem.addEventListener("click", () =>
					archiveEmail(id, archiveValue)
				);

				buttonElem1.addEventListener("click", () => {
					const composeView = document.querySelector("#compose-view");

					composeView.style.display = "block";
					emailView.style.display = "none";
					emailsView.style.display = "none";

					let subject = document.querySelector("#compose-subject");

					document.querySelector("#compose-recipients").value =
						result.sender;

					if (result.subject.toLowerCase().startsWith("re:")) {
						subject.value = `${result.subject}`;
					} else {
						console.log(result.subject);
						subject.value = `Re: ${result.subject}`;
					}

					document.querySelector(
						"#compose-body"
					).value = `On ${result.timestamp} ${result.sender} wrote:\n\n**${result.body}**`;
				});
		});
}

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


function archiveEmail(id, archiveValue) {
	fetch(`/mail/archive/${id}`, {
		method: "PUT",
		credentials: "include",
		headers: {
			"Content-Type": "application/json",
			"X-CSRFToken": getCookie("csrftoken"),
		},

		body: JSON.stringify({ archived: archiveValue }),
	}).then(() => {
		load_mailbox("inbox");
	});
}
