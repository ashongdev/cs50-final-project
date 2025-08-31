document.addEventListener("DOMContentLoaded", () => {
	console.log("Loaded");

	const noteItems = document.querySelectorAll(".note-item");

	noteItems.forEach((note) => {
		note.addEventListener("click", () => {
			const noteId = note.dataset.noteId;

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
					).toLocaleDateString();

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
			}).then((_) => {
				alert("Note Archived");

				window.location.reload();
			});
		});

	const unarchiveBtn = document.querySelector(".unarchive");
	unarchiveBtn &&
		unarchiveBtn.addEventListener("click", () => {
			console.log("sksk");

			const urlParams = new URLSearchParams(window.location.search);
			const noteId = urlParams.get("note_id");

			fetch(`/unarchive_note/${noteId}`, {
				method: "GET",
				headers: { "Content-Type": "application/json" },
				credentials: "include",
			}).then((_) => {
				alert("Note Unarchived");

				window.location.reload();
			});
		});

	const deletedBtn = document.querySelector(".delete");
	deletedBtn &&
		deletedBtn.addEventListener("click", () => {
			console.log("sksk");

			const urlParams = new URLSearchParams(window.location.search);
			const noteId = urlParams.get("note_id");

			fetch(`/delete_note/${noteId}`, {
				method: "GET",
				headers: { "Content-Type": "application/json" },
				credentials: "include",
			}).then((_) => {
				alert("Note deleted");

				window.location.reload();
			});
		});

	const restoreBtn = document.querySelector(".restore");
	restoreBtn &&
		restoreBtn.addEventListener("click", () => {
			console.log("sksk");

			const urlParams = new URLSearchParams(window.location.search);
			const noteId = urlParams.get("note_id");

			fetch(`/restore_note/${noteId}`, {
				method: "GET",
				headers: { "Content-Type": "application/json" },
				credentials: "include",
			}).then((_) => {
				alert("Note restored");

				window.location.reload();
			});
		});
});
