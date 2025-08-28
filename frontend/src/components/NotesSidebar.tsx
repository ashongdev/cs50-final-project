import { Plus } from "lucide-react";
import { Dispatch, FC, SetStateAction, useEffect, useState } from "react";
import { Note } from "../exports";

interface Props {
	setSelectedNote: Dispatch<SetStateAction<Note>>;
}

const NotesSidebar: FC<Props> = ({ setSelectedNote }) => {
	const [notes, setNotes] = useState([
		{
			id: 1,
			title: "React Performance Optimization",
			tags: ["Dev", "React"],
			updated_at: new Date(),
			isActive: false,
			content:
				"Lorem ipsum dolor sit, amet consectetur adipisicing elit. Cum rem, libero quia omnis perferendis minus, voluptas mollitia laudantium nemo odio aliquam veritatis illum fugiat magnam delectus dolorem iusto corporis deleniti.",
		},
		{
			id: 2,
			title: "Japan Travel Planning",
			tags: ["Travel", "Personal"],
			updated_at: new Date(),
			isActive: true,
			content:
				"Lorem ipsum dolor sit, amet consectetur adipisicing elit. Cum rem, libero quia omnis perferendis minus, voluptas mollitia laudantium nemo odio aliquam veritatis illum fugiat magnam delectus dolorem iusto corporis deleniti.",
		},
		{
			id: 3,
			title: "Favorite Pasta Recipes",
			tags: ["Cooking", "Recipes"],
			updated_at: new Date(),
			isActive: false,
			content:
				"Lorem ipsum dolor sit, amet consectetur adipisicing elit. Cum rem, libero quia omnis perferendis minus, voluptas mollitia laudantium nemo odio aliquam veritatis illum fugiat magnam delectus dolorem iusto corporis deleniti.",
		},
		{
			id: 4,
			title: "Weekly Workout Plan",
			tags: ["Dev", "React"],
			updated_at: new Date(),
			isActive: false,
			content:
				"Lorem ipsum dolor sit, amet consectetur adipisicing elit. Cum rem, libero quia omnis perferendis minus, voluptas mollitia laudantium nemo odio aliquam veritatis illum fugiat magnam delectus dolorem iusto corporis deleniti.",
		},
	]);

	useEffect(() => {
		const activeNote = notes.find((note) => note.isActive === true);

		if (activeNote) setSelectedNote(activeNote);
	}, []);

	function toggleActive(id: number) {
		const activeNote = notes.find((note) => note.id === id);

		if (activeNote) {
			setSelectedNote(activeNote);

			setNotes((prevTabs) =>
				prevTabs.map((note) => ({
					...note,
					isActive: note.id === id,
				}))
			);
		}
	}

	return (
		<div className="border-r-1 border-r-gray-200 w-full max-w-[30rem] min-w-[15rem] h-full overflow-x-hidden pt-5 px-2">
			<button className="flex justify-center items-center text-white w-full gap-1 bg-blue-500 transition-all duration-200 hover:bg-blue-700 py-2 rounded-sm cursor-pointer">
				<Plus size={13} />
				<span>Create New Note</span>
			</button>

			<div className="flex flex-col py-3 gap-1">
				{notes.map((note) => (
					<div
						className={`flex justify-between items-center pb-3 pt-1 hover:bg-gray-800/10 transition-all duration-200 cursor-pointer px-2 rounded-sm gap-3 ${
							note.isActive ? "bg-gray-800/10" : ""
						}`}
						key={note.id}
						onClick={() => toggleActive(note.id)}
					>
						<div className="flex justify-center items-start gap-3 flex-col">
							<p className="font-bold text-lg">{note.title}</p>
							<div className="flex justify-start gap-1 w-full items-center">
								{note.tags.map((tag) => (
									<span
										key={tag}
										className="bg-gray-500 px-2 rounded-xs py-1 text-xs text-gray-200"
									>
										{tag}
									</span>
								))}
							</div>

							<p className="text-gray-500 font-semibold text-xs">
								{note.updated_at.toLocaleDateString()}
							</p>
						</div>
					</div>
				))}
			</div>
		</div>
	);
};

export default NotesSidebar;
