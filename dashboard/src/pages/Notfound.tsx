import { useNavigate } from "react-router-dom";

const NotFound = () => {
  const navigate = useNavigate();

  return (
    <div className="h-screen flex items-center justify-center bg-white text-black">
      <div className="text-center space-y-4">
        
        {/* Thin 404 */}
        <h1 className="text-[120px] font-light tracking-tight">
          404
        </h1>

        {/* Subtitle */}
        <p className="text-sm text-gray-600">
          Page Not Found
        </p>

        {/* Back */}
        <button
          onClick={() => navigate("/")}
          className="text-sm text-black hover:opacity-60 transition"
        >
          ← Back to Home
        </button>

      </div>
    </div>
  );
};

export default NotFound;