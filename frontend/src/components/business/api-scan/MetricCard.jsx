import React from "react";
import { Card, CardContent } from "../../ui/card";

const getGradient = (type) => {
  const gradients = {
    critical: "from-red-500 to-orange-500",
    warning: "from-yellow-400 to-orange-300",
    success: "from-green-400 to-emerald-500",
    info: "from-blue-400 to-indigo-500",
  };
  return gradients[type] || gradients.info;
};

const MetricCard = ({ title, value, trend, type, icon: Icon, hoveredCard, setHoveredCard }) => (
  <Card
    className={`relative overflow-hidden transition-all duration-500 transform hover:scale-105 ${
      hoveredCard === title ? "ring-2 ring-offset-2 ring-blue-500" : ""
    }`}
    onMouseEnter={() => setHoveredCard(title)}
    onMouseLeave={() => setHoveredCard(null)}
  >
    <div className={`absolute inset-0 bg-gradient-to-br ${getGradient(type)} opacity-10`} />
    <div className="absolute -right-4 -bottom-4 w-32 h-32 opacity-10">
      <Icon className="w-full h-full" />
    </div>
    <CardContent className="relative p-6 z-10">
      <div className="flex justify-between items-start">
        <div className={`p-3 rounded-xl bg-gradient-to-br ${getGradient(type)}`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
        <span
          className={`
          text-sm font-medium px-2.5 py-1 rounded-full
          ${trend > 0 ? "text-red-500 bg-red-100" : "text-green-500 bg-green-100"}
        `}
        >
          {trend > 0 ? "+" : ""}
          {trend}%
        </span>
      </div>
      <div className="mt-4">
        <h3 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-600">
          {value}
        </h3>
        <p className="text-sm text-gray-500 mt-1">{title}</p>
      </div>
    </CardContent>
  </Card>
);

export default MetricCard;
