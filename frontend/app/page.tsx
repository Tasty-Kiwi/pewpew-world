import LeaderboardExtract from "@/components/leaderboard-extract";

export default function Home() {
  return (
    <div className="container-xl p-4">
      <div className="d-flex justify-content-between align-items-center">
        <div>
          <h2 className="page-title">PewPew World ✨</h2>
          <div className="alert alert-info mt-3" role="alert">
            <div className="alert-icon">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="icon alert-icon icon-2"
              >
                <path d="M3 12a9 9 0 1 0 18 0a9 9 0 0 0 -18 0" />
                <path d="M12 9h.01" />
                <path d="M11 12h1v4h1" />
              </svg>
            </div>
            <div>
              <h4 className="alert-heading">Hey there!</h4>
              <div className="alert-description">
                - This is an unofficial PewPew website. Data here is based on
                official{" "}
                <a href="https://github.com/pewpewlive/ppl-data">ppl-data</a>,
                as well as personal regular scrapes for archives.
                <br />- This website is{" "}
                <a href="https://github.com/artiekra/pewpew-world">
                  open-source
                </a>
                !
              </div>
            </div>
          </div>
        </div>
      </div>
      <div className="row mt-2">
        <div className="col-12 col-md-6 mb-4">
          <LeaderboardExtract type="monthly" />
        </div>
        <div className="col-12 col-md-6 mb-4">
          <LeaderboardExtract type="speedrun" />
        </div>
      </div>
    </div>
  );
}
