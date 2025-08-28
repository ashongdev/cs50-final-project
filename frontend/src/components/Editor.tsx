import axios from "axios";
import { Clock, Tag } from "lucide-react";
import { FC, FormEvent, useEffect, useState } from "react";
import { Note } from "../exports";

interface Props {
	selectedNote: Note;
}

const Editor: FC<Props> = ({ selectedNote }) => {
	const [content, setContent] = useState(selectedNote.content || "");
	const saveNote = async (e: FormEvent<HTMLFormElement>) => {
		e.preventDefault();

		try {
			await axios.post("http://127.0.0.1:8000/create", { content });
		} catch (error) {
			console.log("🚀 ~ saveNote ~ error:", error);
		}
	};

	useEffect(() => {
		if (selectedNote?.content) {
			setContent(selectedNote.content);
		}
	}, [selectedNote]); // run effect whenever selectedNote changes

	return (
		<div className="m-5 whitespace-nowrap">
			{selectedNote && (
				<>
					<div className="border-b-1 pb-5 border-b-gray-200">
						<h1 className="font-bold text-3xl">
							{selectedNote.title}
						</h1>

						<div className="flex gap-5 my-3">
							<div className="flex min-w-[10rem] justify-start items-center gap-2 text-gray-700">
								<Tag size={17} />
								<p>Tags</p>
							</div>
							<p className="text-gray-700">
								{selectedNote.tags.map(
									(tag, index) =>
										`${tag}${
											index + 1 !==
											selectedNote.tags.length
												? ", "
												: ""
										}`
								)}
							</p>
						</div>

						<div className="flex gap-5">
							<div className="flex min-w-[10rem] justify-start items-center gap-2 text-gray-700">
								<Clock size={17} />
								<p>Last edited</p>
							</div>
							<p className="text-gray-700">
								{selectedNote.updated_at?.toLocaleDateString()}
							</p>
						</div>
					</div>

					<form className="h-full" onSubmit={(e) => saveNote(e)}>
						<div className="mt-3 h-full  w-full max-h-[25rem] overflow-y-scroll [scrollbar-width:none] [-ms-overflow-style:none] [&::-webkit-scrollbar]:hidden">
							<textarea
								value={content ? content : "Loading..."}
								className="w-full h-full outline-none resize-none"
								autoFocus={true}
								onChange={(e) => setContent(e.target.value)}
							/>
						</div>

						<div className="mt-5 flex gap-5">
							<button className="bg-blue-600 text-gray-100 cursor-pointer hover:bg-blue-800 transition-all duration-200 px-5 py-2 rounded-md">
								Save Note
							</button>
							<button className="bg-gray-700 text-gray-200 cursor-pointer hover:bg-gray-600 hover:text-white transition-all duration-200 px-5 py-2 rounded-md">
								Cancel
							</button>
						</div>
					</form>
				</>
			)}
		</div>
	);
};

export default Editor;
