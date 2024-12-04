// frontend/src/app/components/TopCompaniesTable.tsx

import Image from "next/image";

export interface Company {
  logo?: string;
  name?: string;
  esgScore?: number;
  amountSpent?: number;
  "Company Name"?: string;
  "ESG Score"?: number;
  "Amount Spent"?: number;
};

const getDomainVariations = (companyName: string) => {
  const name = companyName.toLowerCase().replace(/[^a-z0-9]/g, '');
  return [
    `${name}.com`,
    `${name}.co`,
    `${name}.org`,
    `${name}.net`,
    `${name}corp.com`,
    `${name}inc.com`,
  ];
};

const TopCompaniesTable = ({ companies }: { companies: Company[] | undefined }) => {
  const formatCompanyData = (rawCompanies: Company[]): Company[] => {
    return rawCompanies.map(company => ({
      logo: `https://logo.clearbit.com/${(company["Company Name"] ?? "").toLowerCase()}.com`,
      name: company["Company Name"] ?? "",
      esgScore: company["ESG Score"] ?? 0,
      amountSpent: company["Amount Spent"] ?? 0
    }));
  };

  const LoadingRow = () => (
    <div className="grid grid-cols-3 gap-4 border-b border-stroke dark:border-strokedark">
      <div className="flex items-center justify-center gap-3 p-2.5 xl:p-5">
        <div className="flex-shrink-0 w-12 h-12 rounded-full bg-gray-200 animate-pulse" />
        <div className="w-24 h-4 bg-gray-200 rounded animate-pulse" />
      </div>
      <div className="flex items-center justify-center p-2.5 xl:p-5">
        <div className="w-12 h-4 bg-gray-200 rounded animate-pulse" />
      </div>
      <div className="flex items-center justify-center p-2.5 xl:p-5">
        <div className="w-20 h-4 bg-gray-200 rounded animate-pulse" />
      </div>
    </div>
  );

  return (
    <div className="mt-5 rounded-sm border border-stroke bg-white px-5 pb-2.5 pt-6 shadow-default dark:border-strokedark dark:bg-boxdark sm:px-7.5 xl:pb-1">
      <h1 className="text-3xl font-extrabold text-black dark:text-white">
        Your most purchased-from companies
      </h1>
      <p className="mb-5 pt-4 text-xl">
        See which companies you purchased from the most, and their carbon footprints
      </p>

      <div className="flex flex-col">
        <div className="grid grid-cols-3 gap-4 rounded-sm bg-gray-2 dark:bg-meta-4">
          <div className="p-2.5 text-center xl:p-5">
            <h5 className="text-sm font-medium uppercase xsm:text-base">Company</h5>
          </div>
          <div className="p-2.5 text-center xl:p-5">
            <h5 className="text-sm font-medium uppercase xsm:text-base">ESG Score</h5>
          </div>
          <div className="p-2.5 text-center xl:p-5">
            <h5 className="text-sm font-medium uppercase xsm:text-base">Amount Purchased</h5>
          </div>
        </div>

        {!companies ? (
          <>
            <LoadingRow />
            <LoadingRow />
            <LoadingRow />
            <LoadingRow />
            <LoadingRow />
          </>
        ) : (
          formatCompanyData(companies).map((company, key) => (
            <div
              className={`grid grid-cols-3 gap-4 ${
                key === companies.length - 1
                  ? ""
                  : "border-b border-stroke dark:border-strokedark"
              }`}
              key={key}
            >
              <div className="flex items-center p-2.5 xl:p-5">
                <div className="flex items-center gap-10">
                  <div className="flex-shrink-0 w-12 h-12 border border-gray-200 rounded-full p-0.5 flex items-center justify-center">
                    <Image
                      src={`https://logo.clearbit.com/${getDomainVariations(company.name ?? '')[0]}`}
                      alt={`${company.name ?? 'Company'} logo`}
                      width={40}
                      height={40}
                      className="rounded-full object-contain"
                      onError={(e: React.SyntheticEvent<HTMLImageElement, Event>) => {
                        const target = e.target as HTMLImageElement;
                        const currentDomain = target.src.split('/').pop();
                        const domains = getDomainVariations(company.name ?? '');
                        const currentIndex = domains.findIndex(d => d === currentDomain);
                        if (currentIndex < domains.length - 1) {
                          target.src = `https://logo.clearbit.com/${domains[currentIndex + 1]}`;
                        } else {
                          target.src = '/fallback-logo.png';
                        }
                      }}
                    />
                  </div>
                  <p className="text-black dark:text-white">
                    {company.name}
                  </p>
                </div>
              </div>

              <div className="flex items-center justify-center p-2.5 xl:p-5">
                <p className="text-black dark:text-white">
                  {company.esgScore === 0 ? "N/A" : company.esgScore}
                </p>
              </div>

              <div className="flex items-center justify-center p-2.5 xl:p-5">
                <p className="text-meta-3">${(company.amountSpent ?? 0).toFixed(2)}</p>
              </div>
            </div>
          ))
        )}
      </div>

      <a href="/transactions">
        <button className="mt-5 w-full rounded-2xl border border-stroke bg-green-400 px-5 pb-3 pt-3 font-bold text-white sm:px-7.5 xl:col-span-8 my-4">
            See All Transactions
        </button>
      </a>
    </div>
  );
};

export default TopCompaniesTable;
