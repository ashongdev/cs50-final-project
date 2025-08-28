import { Archive, Trash2Icon } from "lucide-react";

const RightSidebar = () => {
	return (
		<div className="border-l-1 min-w-[10rem] border-l-gray-200 w-full max-w-[30rem] gap-3 flex flex-col h-full overflow-x-hidden pt-5 px-2">
			<button className="flex justify-start pl-3 items-center w-full gap-3 border-1 border-gray-200 transition-all duration-200 hover:bg-blue-700 hover:text-white py-2 rounded-sm cursor-pointer">
				<Archive size={13} />
				<span>Archive Note</span>
			</button>
			<button className="flex justify-start pl-3 items-center w-full gap-3 border-1 border-gray-200 transition-all duration-200 hover:bg-red-700 hover:text-white py-2 rounded-sm cursor-pointer">
				<Trash2Icon size={13} />
				<span>Delete Note</span>
			</button>
		</div>
	);
};

export default RightSidebar;
