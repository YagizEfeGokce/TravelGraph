import { lazy, Suspense } from "react";
import { AuthProvider } from "./contexts/AuthContext";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import ProtectedRoute from "./components/ProtectedRoute";

import Navbar from "./components/Navbar";
import HomePage from "./pages/HomePage";

const ExplorePage = lazy(() => import("./pages/ExplorePage"));
const DestinationDetailPage = lazy(() => import("./pages/DestinationDetailPage"));
const PlannerPage = lazy(() => import("./pages/PlannerPage"));
const BudgetPlannerPage = lazy(() => import("./pages/BudgetPlannerPage"));
const FestivalsPage = lazy(() => import("./pages/FestivalsPage"));
const ProfilePage = lazy(() => import("./pages/ProfilePage"));
const LoginPage = lazy(() => import("./pages/LoginPage"));
const RegisterPage = lazy(() => import("./pages/RegisterPage"));
const NotFoundPage = lazy(() => import("./pages/NotFoundPage"));

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <a
          href="#main-content"
          className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-[60] focus:px-4 focus:py-2 focus:bg-primary focus:text-on-primary focus:rounded-lg focus:font-bold"
        >
          Skip to content
        </a>
        <div className="flex flex-col min-h-screen bg-background">
          <Navbar />
          <main id="main-content" className="flex-1">
            <Suspense fallback={
              <div className="min-h-screen flex items-center justify-center">
                <p className="text-on-surface-variant font-bold">Loading...</p>
              </div>
            }>
              <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/explore" element={<ExplorePage />} />
                <Route path="/destinations/:id" element={<DestinationDetailPage />} />
                <Route path="/planner" element={<ProtectedRoute><PlannerPage /></ProtectedRoute>} />
                <Route path="/planner/:id/budget" element={<ProtectedRoute><BudgetPlannerPage /></ProtectedRoute>} />
                <Route path="/festivals" element={<FestivalsPage />} />
                <Route path="/profile" element={<ProtectedRoute><ProfilePage /></ProtectedRoute>} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
                <Route path="*" element={<NotFoundPage />} />
              </Routes>
            </Suspense>
          </main>
        </div>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
