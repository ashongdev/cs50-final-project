type Note = {
	id: number | null;
	title: string;
	tags: string[];
	updated_at: Date | null;
	isActive: boolean;
	content: string;
};

export { Note };
