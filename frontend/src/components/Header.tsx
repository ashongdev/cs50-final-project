import { Search, Settings } from "lucide-react";

const Header = () => {
	return (
		<header className="flex w-full border-b-1 border-b-gray-200 p-5 justify-between items-center">
			<h1 className="font-bold text-2xl">All Notes</h1>

			<div className="flex items-center justify-start min-w-[20rem] gap-5">
				<div className="flex items-center justify-center relative">
					<span className="text-gray-600 absolute left-3">
						<Search size={17} />
					</span>
					<input
						className="w-[20rem] placeholder:text-sm border-2 outline-0 focus:border-3 focus:border-blue-500 border-gray-200 px-10 py-2 rounded-sm"
						type="text"
						placeholder="Search by title, content, or tags..."
					/>
				</div>

				<span className="text-gray-600 cursor-pointer">
					<Settings size={17} />
				</span>
			</div>
		</header>
	);
};

export default Header;
