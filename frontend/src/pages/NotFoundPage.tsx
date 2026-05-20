import { Link } from "react-router-dom";

function NotFoundPage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-background text-on-surface">
      <h1 className="text-6xl font-black font-headline mb-4">404</h1>
      <p className="text-lg text-on-surface-variant mb-8">Page not found</p>
      <Link
        to="/"
        className="px-6 py-3 bg-primary text-on-primary rounded-xl font-bold hover:opacity-90 transition-opacity"
      >
        Go Home
      </Link>
    </div>
  );
}

export default NotFoundPage;
