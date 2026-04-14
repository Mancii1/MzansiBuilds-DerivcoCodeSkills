const Footer = () => {
  return (
    <footer className="bg-white border-t border-gray-100 py-8">
      <div className="container mx-auto px-4 text-center">
        <p className="text-gray-600">
          © {new Date().getFullYear()} MzansiBuilds. Built by South African developers, for South African developers.
        </p>
        <p className="text-sm text-gray-500 mt-2">
          🇿🇦 Proudly Mzansi
        </p>
      </div>
    </footer>
  );
};

export default Footer;
