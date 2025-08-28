import Editor from "@/components/Editor";
import Header from "@/components/Header";
import NotesSidebar from "@/components/NotesSidebar";
import PrimarySidebar from "@/components/PrimarySidebar";
import RightSidebar from "@/components/RightSidebar";
import { useAuth } from "@/context/AuthContext";
import { Note } from "@/exports";
import { useState } from "react";

export const Home = () => {
	const [selectedNote, setSelectedNote] = useState<Note>({
		id: null,
		title: "",
		tags: [],
		updated_at: null,
		isActive: false,
		content: "",
	});

	const { user } = useAuth();
	console.log(user);

	return (
		<div className="w-full h-full flex text-gray-800">
			<PrimarySidebar />

			<main className="w-full">
				<Header />

				<section className="grid grid-cols-[0.4fr_1fr_0.4fr] w-full h-full ">
					<NotesSidebar setSelectedNote={setSelectedNote} />

					<Editor selectedNote={selectedNote} />

					<RightSidebar />
				</section>
			</main>
		</div>
	);
};

export default Home;
