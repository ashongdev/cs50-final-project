"use client";

import ThirdPartyAuth from "@/components/ThirdPartyAuth";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { Link } from "react-router-dom";
import { z } from "zod";

const formSchema = z.object({
	username: z.string().min(2).max(50),
	password: z.string().min(8),
});
const Signup = () => {
	const form = useForm<z.infer<typeof formSchema>>({
		resolver: zodResolver(formSchema),
		defaultValues: {
			username: "",
			password: "",
		},
	});

	// 2. Define a submit handler.
	function onSubmit(values: z.infer<typeof formSchema>) {
		// Do something with the form values.
		// ✅ This will be type-safe and validated.
		console.log(values);
	}

	return (
		<>
			<div className="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
				<div className="sm:mx-auto sm:w-full sm:max-w-sm">
					<h2 className="mt-10 text-center text-2xl/9 font-bold tracking-tight text-gray-800">
						Create a New Account
					</h2>
				</div>

				<div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
					<form action="#" method="POST" className="space-y-6">
						<div>
							<label
								htmlFor="email"
								className="block text-sm/6 font-medium text-gray-800"
							>
								Email address
							</label>
							<div className="mt-2">
								<input
									id="email"
									type="email"
									name="email"
									required
									autoComplete="email"
									placeholder="Enter your email address"
									className="block w-full rounded-md bg-white/5 px-3 py-1.5 text-base text-gray-800 outline-1 -outline-offset-1 outline-white/10 border-1 border-gray-300 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500 sm:text-sm/6"
								/>
							</div>
						</div>

						<div>
							<div className="flex items-center justify-between">
								<label
									htmlFor="password"
									className="block text-sm/6 font-medium text-gray-800"
								>
									Password
								</label>
							</div>
							<div className="mt-2">
								<input
									id="password"
									type="password"
									name="password"
									required
									placeholder="Enter your password"
									autoComplete="current-password"
									className="block w-full rounded-md bg-white/5 px-3 py-1.5 text-base text-gray-800 outline-1 -outline-offset-1 outline-white/10 border-1 border-gray-300 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500 sm:text-sm/6"
								/>
							</div>
						</div>
						<div>
							<div className="flex items-center justify-between">
								<label
									htmlFor="confirmPassword"
									className="block text-sm/6 font-medium text-gray-800"
								>
									Confirm Password
								</label>
							</div>
							<div className="mt-2">
								<input
									id="confirmPassword"
									type="confirmPassword"
									name="confirmPassword"
									required
									placeholder="Re-enter your password"
									autoComplete="current-confirmPassword"
									className="block w-full rounded-md bg-white/5 px-3 py-1.5 text-base text-gray-800 outline-1 -outline-offset-1 outline-white/10 border-1 border-gray-300 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500 sm:text-sm/6"
								/>
							</div>
						</div>

						<div>
							<button
								type="submit"
								className="flex w-full justify-center rounded-md bg-indigo-500 px-3 py-1.5 text-sm/6 font-semibold text-white hover:bg-indigo-400 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500 cursor-pointer"
							>
								Sign up
							</button>
						</div>
					</form>

					<p className="mt-10 text-center text-sm/6 text-gray-400">
						Already have an account?{" "}
						<Link
							to="/signin"
							className="font-semibold text-indigo-400 hover:text-indigo-300"
						>
							Sign in
						</Link>
					</p>

					<ThirdPartyAuth auth="Sign up" />
				</div>
			</div>
		</>
	);
};

export default Signup;
