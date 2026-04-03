{
  description = "Shell for smlp";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs  }: {
    devShells.x86_64-linux.default = let
      pkgs = nixpkgs.legacyPackages.x86_64-linux;

    in pkgs.mkShell {
      nativeBuildInputs = [
        pkgs.pkg-config
        pkgs.ninja
        pkgs.cmake
        pkgs.python311
        pkgs.hdf5
        pkgs.flint
        pkgs.z3
      ];

      buildInputs = [
        pkgs.meson
        pkgs.python311Packages.boost
        pkgs.gmp
        pkgs.gmpxx
      ];

      shellHook = ''
        export BOOST_INCLUDEDIR=${pkgs.lib.getDev pkgs.python311Packages.boost}/include
        export BOOST_LIBRARYDIR=${pkgs.lib.getLib pkgs.python311Packages.boost}/lib

        export LD_LIBRARY_PATH="${pkgs.lib.getLib pkgs.gmp}/lib:/home/kirkm/kjson/lib:${pkgs.lib.getLib pkgs.z3}/lib:${pkgs.lib.getLib pkgs.hdf5}/lib"
      '';
    };
  };
}
