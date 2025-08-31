document.addEventListener("DOMContentLoaded", () => {
	function removeParam(paramName, urlParams) {
		if (!urlParams) return;
		const url = new URL(window.location.href);

		urlParams.delete(paramName);
		url.search = urlParams.toString();
		history.pushState("", null, url.toString());
	}

	const urlParams = new URLSearchParams(window.location.search);
	removeParam("note_id", urlParams);

	const noteItems = document.querySelectorAll(".note-item");

	noteItems.forEach((note) => {
		note.addEventListener("click", () => {
			const noteId = note.dataset.noteId;

			const urlParams = new URLSearchParams(window.location.search);
			const noteParamId = urlParams.get("note_id");

			// Prevent unnecessary api calls
			if (noteId === noteParamId) {
				return;
			}

			document.querySelector(".placeholder-text").style.display = "none";
			document.querySelector(".toggle").style.display = "block";
			document.querySelector(".right-sidebar").style.display = "flex";

			history.pushState("", null, `?note_id=${noteId}`);

			fetch(`/select_note/${noteId}`, {
				method: "GET",
				headers: { "Content-Type": "application/json" },
				credentials: "include",
			}).then((response) => {
				response.json().then((result) => {
					const title = document.querySelector(".editor-title");
					const updatedAt = document.querySelector(".updated-at");
					const contentArea = document.querySelector(".content");

					const noteDetails = result.note_details;
					title.innerHTML = noteDetails.title;
					updatedAt.innerHTML = new Date(
						noteDetails.updated_at
					).toDateString();

					const tags = document.querySelector(".meta-tags");
					tags.innerHTML = "";
					noteDetails.tags.forEach((tag, index) => {
						tags.innerHTML += `${tag}${
							index === noteDetails.tags.length - 1 ? "" : ", "
						}`;
					});

					contentArea.value = noteDetails.content;
				});
			});
		});
	});

	const archiveBtn = document.querySelector(".archive");
	archiveBtn &&
		archiveBtn.addEventListener("click", () => {
			const urlParams = new URLSearchParams(window.location.search);
			const noteId = urlParams.get("note_id");

			fetch(`/archive_note/${noteId}`, {
				method: "GET",
				headers: { "Content-Type": "application/json" },
				credentials: "include",
			}).then((response) => {
				if (response.ok) {
					removeParam("note_id", urlParams);
				}
			});
		});

	const unarchiveBtn = document.querySelector(".unarchive");
	unarchiveBtn &&
		unarchiveBtn.addEventListener("click", () => {
			const urlParams = new URLSearchParams(window.location.search);
			const noteId = urlParams.get("note_id");

			fetch(`/unarchive_note/${noteId}`, {
				method: "GET",
				headers: { "Content-Type": "application/json" },
				credentials: "include",
			}).then((response) => {
				if (response.ok) {
					removeParam("note_id", urlParams);
				}
			});
		});

	const deletedBtn = document.querySelector(".delete");
	deletedBtn &&
		deletedBtn.addEventListener("click", () => {
			const urlParams = new URLSearchParams(window.location.search);
			const noteId = urlParams.get("note_id");

			fetch(`/delete_note/${noteId}`, {
				method: "GET",
				headers: { "Content-Type": "application/json" },
				credentials: "include",
			}).then((response) => {
				if (response.ok) {
					removeParam("note_id", urlParams);
				}
			});
		});

	const restoreBtn = document.querySelector(".restore");
	restoreBtn &&
		restoreBtn.addEventListener("click", () => {
			const urlParams = new URLSearchParams(window.location.search);
			const noteId = urlParams.get("note_id");

			fetch(`/restore_note/${noteId}`, {
				method: "GET",
				headers: { "Content-Type": "application/json" },
				credentials: "include",
			}).then((response) => {
				if (response.ok) {
					removeParam("note_id", urlParams);
				}
			});
		});

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

	const editorForm = document.querySelector(".editor-form");
	editorForm &&
		editorForm.addEventListener("submit", (e) => {
			e.preventDefault();
			const urlParams = new URLSearchParams(window.location.search);
			const noteId = urlParams.get("note_id");
			const title = document.querySelector(".editor-title");
			const tags = document.querySelector(".meta-tags");
			const contentArea = document.querySelector(".content");
			// const saveBtn = document.querySelector(".save")

			fetch(`/save_note/${noteId}`, {
				method: "POST",
				body: JSON.stringify({
					content: contentArea.value,
					title: title.innerHTML,
					tags: tags.innerHTML,
				}),
				headers: {
					"Content-Type": "application/json",
					"X-CSRFToken": getCookie("csrftoken"),
				},
				credentials: "include",
			}).then((response) => {
				if (response.ok) {
					// alert("Saved");
					window.location.reload();

					// removeParam("note_id", urlParams);
				}
			});

			console.log("Submitted");
		});

	const editorTitleBtn = document.querySelector(".edit-title-btn");
	editorTitleBtn &&
		editorTitleBtn.addEventListener("click", () => {
			document.querySelector(".editor-title").style.display = "none";
			editorTitleBtn.style.display = "none";

			document.querySelector(".edit-title-cont").style.display = "flex";
			document.querySelector(".edit-title-input").value =
				document.querySelector(".editor-title").innerHTML;
		});

	const cancelTitleEditBtn = document.querySelector(".edit-title-cancel");
	cancelTitleEditBtn &&
		cancelTitleEditBtn.addEventListener("click", () => {
			document.querySelector(".editor-title").style.display = "initial";
			editorTitleBtn.style.display = "initial";

			document.querySelector(".edit-title-cont").style.display = "none";
			document.querySelector(".edit-title-input").value =
				document.querySelector(".editor-title").innerHTML;
		});

	const saveTitleEditBtn = document.querySelector(".edit-title-save");
	saveTitleEditBtn &&
		saveTitleEditBtn.addEventListener("click", () => {
			document.querySelector(".editor-title").style.display = "initial";
			editorTitleBtn.style.display = "initial";

			document.querySelector(".edit-title-cont").style.display = "none";
			document.querySelector(".editor-title").innerHTML =
				document.querySelector(".edit-title-input").value;
		});

	// Tags edit
	const editorTagsBtn = document.querySelector(".edit-tags-btn");
	editorTagsBtn &&
		editorTagsBtn.addEventListener("click", () => {
			document.querySelector(".meta-tags").style.display = "none";
			editorTagsBtn.style.display = "none";

			document.querySelector(".edit-tags-cont").style.display = "flex";
			document.querySelector(".edit-tags-input").value =
				document.querySelector(".meta-tags").innerHTML;
		});

	const cancelTagsEditBtn = document.querySelector(".edit-tags-cancel");
	cancelTagsEditBtn &&
		cancelTagsEditBtn.addEventListener("click", () => {
			document.querySelector(".meta-tags").style.display = "initial";
			editorTagsBtn.style.display = "initial";

			document.querySelector(".edit-tags-cont").style.display = "none";
			document.querySelector(".edit-tags-input").value =
				document.querySelector(".editor-tags").innerHTML;
		});

	const saveTagsEditBtn = document.querySelector(".edit-tags-save");
	saveTagsEditBtn &&
		saveTagsEditBtn.addEventListener("click", () => {
			document.querySelector(".meta-tags").style.display = "initial";
			editorTagsBtn.style.display = "initial";

			document.querySelector(".edit-tags-cont").style.display = "none";
			document.querySelector(".meta-tags").innerHTML =
				document.querySelector(".edit-tags-input").value;
		});
});
