import { Archive, ChevronRight, Home, Tag } from "lucide-react";
import { useState } from "react";
const PrimarySidebar = () => {
	const [tabs, setTabs] = useState([
		{ label: "All Notes", icon: <Home size={17} />, isActive: true },
		{
			label: "Archived Notes",
			icon: <Archive size={17} />,
			isActive: false,
		},
	]);

	function toggleActive(label: string) {
		const activeTab = tabs.find((t) => t.label === label);

		if (activeTab) {
			setTabs((prevTabs) =>
				prevTabs.map((tab) => ({
					...tab,
					isActive: tab.label === label,
				}))
			);
		}
	}

	const tags = ["Cooking", "Dev", "Fitness", "Health", "Personal"];
	return (
		<div className=" left-0 top-0 bottom-0 border-r-1 border-r-gray-200 w-3xs min-w-[15rem] max-w-[30rem] h-full">
			<h1 className="flex justify-start items-center text-3xl p-5 py-3">
				Logo
			</h1>

			<div className="mt-5 mx-3 flex  flex-col border-b-1 border-b-gray-200 py-3 gap-1">
				{tabs.map((s) => (
					<div
						className={`flex justify-between items-center py-2 hover:bg-gray-800/10 transition-all duration-75 cursor-pointer px-5 rounded-sm gap-3 ${
							s.isActive ? "bg-gray-800/10" : ""
						}`}
						key={s.label}
						onClick={() => toggleActive(s.label)}
					>
						<div className="flex justify-center items-center gap-3">
							<span
								className={`${
									s.isActive ? "text-blue-600" : ""
								}`}
							>
								{s.icon}
							</span>
							<span>{s.label}</span>
						</div>
						{s.isActive && <ChevronRight size={15} />}
					</div>
				))}
			</div>

			<div className="mt-5 mx-3 flex  flex-col py-3">
				{tags.map((tag) => (
					<div
						className="flex justify-start items-center py-2 hover:bg-gray-800/10 transition-all duration-75 cursor-pointer px-5 rounded-sm gap-3"
						key={tag}
					>
						<Tag size={17} />
						<span>{tag}</span>
					</div>
				))}
			</div>
		</div>
	);
};

export default PrimarySidebar;
