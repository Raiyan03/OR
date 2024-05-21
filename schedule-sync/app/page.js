import React from "react";
import Image from "next/image";
import Link from "next/link";
import Footer from "./page-components/footer";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-gray-800">
      <Footer />
      <div className="absolute top-0 m-4">
        <h1 className="pt-1 font-bold text-lg">Schedule Sync</h1>
        <h1>"Company Logo?</h1>
        {/*
          <Image src="/" alt="" width={} height={} className=""/>
        */}
      </div>
 
      <div className="w-80 bg-white shadow-md rounded-lg p-8">
        
        <h1 className="text-2xl font-semibold mb-6 text-black">Sign In</h1>
        <div className="mb-4">
          <input
            type="text"
            placeholder="Email or Phone"
            className="w-full py-2 px-3 border border-black rounded-md text-black"
          />
        </div>
        <div className="mb-4">
          <input
            type="text"
            placeholder="Password"
            className="w-full py-2 px-3 border border-black rounded-lg text-black"
          />
        </div>
        <div className="mb-4">
          <Link href="/create-account">
            <span className="text-blue-500 hover:underline">Forgot Password?</span>
          </Link>
        </div>
        <Link href="">
          <button className="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-md w-full">
            Sign In
          </button>
        </Link>
      </div>
      <div className="mt-4 text-center">
        <Link href="/create-account">
          <span className="text-blue-500 hover:underline">Create an account</span>
        </Link>
      </div>  
    </main>
  );
}
