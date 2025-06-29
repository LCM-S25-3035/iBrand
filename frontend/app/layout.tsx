import type { Metadata } from "next";
import "./globals.css";

import ReduxProvider from "../store/ReduxProvider";


export const metadata: Metadata = {
  title: "iBrand",
  description: "AI Brand Messaging Assistant",
  generator: "v0.dev",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <ReduxProvider>{children}</ReduxProvider>
      </body>
    </html>
  );
}
