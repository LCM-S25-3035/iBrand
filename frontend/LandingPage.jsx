import React from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";

const LandingPage = () => {
  return (
    <div className="min-h-screen flex flex-col relative overflow-hidden">
      {/* Animated Gradient Background */}
      <div className="absolute inset-0 animate-gradient bg-gradient-to-br from-blue-500 via-purple-600 to-pink-500"></div>
      <style>
        {`
          .animate-gradient {
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
          }
          @keyframes gradientShift {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
          }
        `}
      </style>

      {/* Floating Shapes */}
      <motion.div
        className="absolute w-32 h-32 bg-white/10 rounded-full blur-2xl"
        animate={{ x: [0, 50, -50, 0], y: [0, -30, 30, 0] }}
        transition={{ repeat: Infinity, duration: 12, ease: "easeInOut" }}
        style={{ top: "10%", left: "15%" }}
      />
      <motion.div
        className="absolute w-40 h-40 bg-white/10 rounded-full blur-2xl"
        animate={{ x: [0, -40, 40, 0], y: [0, 30, -30, 0] }}
        transition={{ repeat: Infinity, duration: 18, ease: "easeInOut" }}
        style={{ bottom: "20%", right: "10%" }}
      />
      <motion.div
        className="absolute w-20 h-20 bg-white/20 rounded-full blur-xl"
        animate={{ y: [0, -20, 20, 0] }}
        transition={{ repeat: Infinity, duration: 10, ease: "easeInOut" }}
        style={{ top: "50%", left: "70%" }}
      />

      {/* Content Layer */}
      <div className="relative z-10 flex flex-col min-h-screen">
        {/* Navbar */}
        <nav className="flex justify-between items-center p-6 bg-white/20 backdrop-blur-md shadow-md">
          <div className="flex items-center space-x-2">
            <img src="/logo.png" alt="iBrand Logo" className="h-8 w-8" />
            <span className="text-xl font-bold text-white">iBrand</span>
          </div>
          <div className="space-x-6">
            <Link to="/dashboard" className="text-white hover:text-gray-200">
              Dashboard
            </Link>
            <Link to="/about" className="text-white hover:text-gray-200">
              About
            </Link>
            <Link to="/login" className="text-white hover:text-gray-200">
              Login
            </Link>
          </div>
        </nav>

        {/* Hero Section */}
        <main className="flex flex-1 flex-col items-center justify-center text-center px-4">
          <motion.h1
            className="text-4xl md:text-6xl font-bold text-white mb-4 drop-shadow-lg"
            initial={{ opacity: 0, y: -50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            Turn News into Social Content with AI
          </motion.h1>

          <motion.p
            className="text-lg md:text-xl text-white max-w-xl mb-6 opacity-90"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.3 }}
          >
            Automate content creation with AI-powered NLP—transform news articles into social-ready posts instantly.
          </motion.p>

          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ duration: 0.5, delay: 0.6 }}
          >
            <Link
              to="/dashboard"
              className="px-6 py-3 bg-white text-blue-700 text-lg rounded-lg shadow-lg hover:bg-gray-100 transition transform hover:scale-105"
            >
              Try it Now
            </Link>
          </motion.div>
        </main>

        {/* Footer */}
        <motion.footer
          className="p-4 text-center text-white text-sm bg-black/30 backdrop-blur-md"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8, delay: 1 }}
        >
          © {new Date().getFullYear()} iBrand. All rights reserved.
        </motion.footer>
      </div>
    </div>
  );
};

export default LandingPage;
