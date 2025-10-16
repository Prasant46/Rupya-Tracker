export const About = () => {
  return (
    <section class="prose md:prose-xl dark:text-white">
      <img
        className="border-[.5px] border-gray-400 p-2"
        height="auto"
        width="100%"
        src="/thumbnail.jpg"
        alt="RupyaTrack - Thumbnail"
      />

      <p className="dark:text-gray-300">
        RupyaTrack is a user-friendly expense tracker app that helps you
        effortlessly manage and monitor your spending habits. Stay organized and
        gain insights into your financial health with RupyaTrack. Try it now!
      </p>

      <h3 className="dark:text-white" id="project-created-at">
        Project Created at
      </h3>
      <ul>
        <li>
          🗓 <em>March 2025 - April 2025</em>
        </li>
      </ul>
      <h3 className="dark:text-white" id="technologies-used-⚒️">
        Technologies Used ⚒️
      </h3>
      <ul>
        <li>Vite + React.js</li>
        <li>Tailwindcss</li>
        <li>React-Query</li>
        <li>Zustand</li>
        <li>React-Hook-Form</li>
        <li>Flask</li>
      </ul>
      <h3 className="dark:text-white" id="features">
        Features
      </h3>
      <ul>
        <li>📧 Authentication: Email + password </li>
        <li>🌐 Social login: Google and GitHub </li>
        <li>🌑 Dark theme functionality </li>
        <li>🗑️ Trash feature </li>
        <li>✏️ Expense management: Create, read, delete, update </li>
        <li>📥 Download expenses as PDF: Filtered by date range </li>
        <li>🔍 Search functionality </li>
        <li>📅 Today&#39;s expenses: Displayed with total amount</li>
      </ul>
    </section>
  );
};
