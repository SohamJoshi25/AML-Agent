import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div className="bg-gray-50 text-gray-900">
      {/* HERO */}
      <section className="max-w-6xl mx-auto px-6 py-20 text-center">
        <h1 className="text-4xl md:text-5xl font-semibold tracking-tight mb-6">
          Detect Fraud.  
          <span className="block text-gray-400">
            Decide with Confidence.
          </span>
        </h1>

        <p className="text-lg text-gray-600 max-w-2xl mx-auto mb-8">
          Real-time transaction monitoring with AI-powered insights and human-in-the-loop verification.
        </p>

        <div className="flex justify-center gap-3">
          <Link
            to="/dashboard"
            className="px-5 py-2.5 bg-gray-900 text-white rounded-md text-sm font-medium hover:bg-gray-800 transition"
          >
            Go to Dashboard
          </Link>

          <a
            href="#features"
            className="px-5 py-2.5 border border-gray-300 rounded-md text-sm font-medium hover:bg-gray-100 transition"
          >
            Learn More
          </a>
        </div>
      </section>

      {/* FEATURES */}
      <section
        id="features"
        className="max-w-6xl mx-auto px-6 pb-20 grid md:grid-cols-3 gap-6"
      >
        {[
          {
            title: "Real-time Monitoring",
            desc: "Stream and analyze transactions instantly with live updates.",
          },
          {
            title: "Explainable AI",
            desc: "Understand why a transaction is flagged with clear reasoning and patterns.",
          },
          {
            title: "Human Verification",
            desc: "Take control with manual review and confirmation workflows.",
          },
        ].map((f) => (
          <div
            key={f.title}
            className="bg-white border border-gray-200 rounded-xl p-5 hover:shadow-sm transition"
          >
            <h3 className="font-semibold text-base mb-2">{f.title}</h3>
            <p className="text-sm text-gray-600">{f.desc}</p>
          </div>
        ))}
      </section>

      {/* CTA */}
      <section className="border-t border-gray-200 bg-white">
        <div className="max-w-6xl mx-auto px-6 py-12 flex flex-col md:flex-row items-center justify-between gap-4">
          <div>
            <h2 className="text-xl font-semibold">
              Ready to review suspicious activity?
            </h2>
            <p className="text-sm text-gray-500">
              Jump into your dashboard and start analyzing transactions.
            </p>
          </div>

          <Link
            to="/dashboard"
            className="px-5 py-2.5 bg-gray-900 text-white rounded-md text-sm font-medium hover:bg-gray-800 transition"
          >
            Open Dashboard
          </Link>
        </div>
      </section>
    </div>
  );
}