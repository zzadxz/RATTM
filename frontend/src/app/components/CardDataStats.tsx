import React, { ReactNode } from "react";

interface CardDataStatsProps {
  title: string;
  total: string;
  circleColor: string;
  children: ReactNode;
  onHoverChange: (isHovered: boolean) => void;
}

const CardDataStats: React.FC<CardDataStatsProps> = ({
  title,
  total,
  circleColor,
  children,
  onHoverChange,
}) => {
  return (
    <div className="relative rounded-2xl border border-stroke bg-white px-7.5 py-6 dark:border-strokedark dark:bg-boxdark">
      {children}

      <div className="mt-4 flex items-end justify-between">
        <div>
          <h4 className="text-title-md font-bold text-black dark:text-white">
            {total}
          </h4>
          <span className="text-sm font-medium">{title}</span>
        </div>

        <span
          className="flex items-center gap-1 text-sm font-medium relative"
          onMouseEnter={() => onHoverChange(true)}
          onMouseLeave={() => onHoverChange(false)}
        >
          <svg
            className="transition-transform duration-300 hover:scale-110"
            width="20"
            height="20"
            viewBox="0 0 10 10"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <circle cx="5" cy="5" r="5" fill="#08d116" />
            <text
              x="5"
              y="5"
              textAnchor="middle"
              dy=".3em"
              fontSize="6"
              fill="white"
            >
              ?
            </text>
          </svg>
        </span>
      </div>
    </div>
  );
};

export default CardDataStats;