// https://www.tiny.cloud/my-account/domains/

tinymce.init({
	selector: "#mytextarea",
	license_key: "gpl",
	origin: "http://127.0.0.1:8000",
	plugins: [
		"a11ychecker",
		"accordion",
		"advlist",
		"anchor",
		"autolink",
		"autosave",
		"charmap",
		"code",
		"codesample",
		"directionality",
		"emoticons",
		"exportpdf",
		"exportword",
		"fullscreen",
		"help",
		"image",
		"importcss",
		"importword",
		"insertdatetime",
		"link",
		"lists",
		"markdown",
		"math",
		"media",
		"nonbreaking",
		"pagebreak",
		"preview",
		"quickbars",
		"save",
		"searchreplace",
		"table",
		"visualblocks",
		"visualchars",
		"wordcount",
	],
	toolbar:
		"undo redo | accordion accordionremove | " +
		"importword exportword exportpdf | math | " +
		"blocks fontfamily fontsize | bold italic underline strikethrough | " +
		"align numlist bullist | link image | table media | " +
		"lineheight outdent indent | forecolor backcolor removeformat | " +
		"charmap emoticons | code fullscreen preview | save print | " +
		"pagebreak anchor codesample | ltr rtl",
	menubar: "file edit view insert format tools table help",
});
