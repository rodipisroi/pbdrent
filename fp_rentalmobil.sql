-- phpMyAdmin SQL Dump
-- version 4.5.1
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: 26 Des 2024 pada 13.16
-- Versi Server: 10.1.19-MariaDB
-- PHP Version: 5.6.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `fp_rentalmobil`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `admin`
--

CREATE TABLE `admin` (
  `admin_id` int(11) NOT NULL,
  `username` varchar(16) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `admin`
--

INSERT INTO `admin` (`admin_id`, `username`, `password`) VALUES
(1, 'syahrul', '123'),
(2, 'rodip', 'rentalmobil');

-- --------------------------------------------------------

--
-- Struktur dari tabel `daftar_mobil`
--

CREATE TABLE `daftar_mobil` (
  `kode_mobil` varchar(10) NOT NULL,
  `merk` varchar(30) NOT NULL,
  `bahan_bakar` enum('bensin','listrik','diesel') NOT NULL,
  `gambar` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `daftar_mobil`
--

INSERT INTO `daftar_mobil` (`kode_mobil`, `merk`, `bahan_bakar`, `gambar`) VALUES
('crv1801', 'Honda CR-V 2017', 'bensin', 'crv2018.png'),
('crv1802', 'Honda CR-V 2018 Matic', 'bensin', 'crv2018.png'),
('day1701', 'Daihatsu Ayla 2017', 'bensin', 'ayla2017.png'),
('inv2101', 'Toyota Innova 2021', 'diesel', 'inv2021.png'),
('jzz1301', 'Honda Jazz 2013', 'bensin', 'jazz2013.png'),
('njk1301', 'Nissan Juke 2013 RX AT', 'bensin', 'juke2013.png'),
('rsh1401', 'Toyota Rush 2014', 'bensin', 'rush2014.png'),
('rtg1701', 'Suzuki Ertiga 2017', 'bensin', 'ertiga2017.png'),
('TYGT86', 'TOYOTA GT86', 'bensin', 'pngwing.com.png'),
('vlz1901', 'Toyota Veloz 2019', 'bensin', 'veloz2019.png'),
('wae2401', 'Wuling Air EV 2024', 'listrik', 'wulingairev.png');

-- --------------------------------------------------------

--
-- Struktur dari tabel `detail_mobil`
--

CREATE TABLE `detail_mobil` (
  `kode_mobil` varchar(10) NOT NULL,
  `plat_no` varchar(12) NOT NULL,
  `sewa_per_hari` int(11) NOT NULL,
  `status` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `detail_mobil`
--

INSERT INTO `detail_mobil` (`kode_mobil`, `plat_no`, `sewa_per_hari`, `status`) VALUES
('crv1801', 'AA1111YY', 200000, 'Ready'),
('crv1801', 'AA2222QQ', 200000, 'Maintenance'),
('crv1802', 'AB2632IE', 250000, 'Ready'),
('TYGT86', 'AG3636BB', 500000, 'Ready'),
('day1701', 'AG7777Y', 225000, 'Ready'),
('vlz1901', 'B1626ER', 250000, 'Ready'),
('rsh1401', 'B7622MM', 250000, 'Ready'),
('inv2101', 'K1877J', 200000, 'Ready'),
('TYGT86', 'K8373QQ', 500000, 'Ready'),
('jzz1301', 'N8927NB', 175000, 'Ready'),
('wae2401', 'Z1234PO', 275000, 'Ready');

-- --------------------------------------------------------

--
-- Struktur dari tabel `driver`
--

CREATE TABLE `driver` (
  `id_driver` int(6) NOT NULL,
  `name` varchar(50) NOT NULL,
  `alamat` varchar(30) NOT NULL,
  `phone` varchar(13) NOT NULL,
  `tahun_lahir` int(4) NOT NULL,
  `lisensi` varchar(10) NOT NULL,
  `sewa_per_hari` int(11) NOT NULL,
  `image` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `driver`
--

INSERT INTO `driver` (`id_driver`, `name`, `alamat`, `phone`, `tahun_lahir`, `lisensi`, `sewa_per_hari`, `image`) VALUES
(10001, 'Elon Musk', 'USA', '082882337821', 1990, 'SIM A', 50000, 'musk.jpg'),
(10002, 'Erik Ten Hag', 'Manchester', '0878387192178', 1977, 'SIM B1', 60000, 'eth.jpg'),
(10003, 'Spongebob Squarepants', 'Bikini Bottom', '081231231783', 2001, 'SIM A', 50000, 'spongebob.jpg'),
(10004, 'Patrick Star', 'Bikini Bottom', '087654321876', 2001, 'SIM B1', 70000, 'patrick.png'),
(10005, 'Darwin Nunez', 'Liverpool', '087898321745', 2000, 'SIM A', 50000, 'nunez.jpeg');

-- --------------------------------------------------------

--
-- Struktur dari tabel `keranjang`
--

CREATE TABLE `keranjang` (
  `id_order` int(11) NOT NULL,
  `id_pelanggan` int(11) NOT NULL,
  `kode_mobil` varchar(8) NOT NULL,
  `merk` varchar(50) NOT NULL,
  `mobil_per_hari` int(11) NOT NULL,
  `id_driver` int(5) NOT NULL,
  `name` varchar(50) NOT NULL,
  `driver_per_hari` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `keranjang`
--

INSERT INTO `keranjang` (`id_order`, `id_pelanggan`, `kode_mobil`, `merk`, `mobil_per_hari`, `id_driver`, `name`, `driver_per_hari`) VALUES
(6, 1, 'day1701', 'Daihatsu Ayla 2017', 225000, 10003, 'Spongebob Squarepants', 50000);

-- --------------------------------------------------------

--
-- Struktur dari tabel `pelanggan`
--

CREATE TABLE `pelanggan` (
  `id_pelanggan` int(6) NOT NULL,
  `nama` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(32) NOT NULL,
  `no_hp` varchar(13) NOT NULL,
  `alamat` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `pelanggan`
--

INSERT INTO `pelanggan` (`id_pelanggan`, `nama`, `email`, `password`, `no_hp`, `alamat`) VALUES
(1, 'Syahrul', 'syahrul@gmail.com', '123', '081234567890', 'Jl. Kemuning No. 92 Jakarta Barat'),
(2, 'tes', 'tes@gmail.com', 'tes', '087654231211', 'Kediri'),
(3, 'khoirul', 'khoirul@gmail.com', '123', '', ''),
(5, 'riski', 'riski@gmail.com', '123', '', ''),
(7, 'nauval', 'nauval@gmail.com', '123', '', ''),
(31, 'Rodif', 'rodif@gmail.com', '1', '', ''),
(32, 'rodip', 'rullsyahrul86@gmai.com', '7', '', ''),
(33, 'rodif', 'rodipp@gmail.com', '123', '', ''),
(34, 'Rodif', 'rodip123@gmail.com', '123', '', '');

-- --------------------------------------------------------

--
-- Struktur dari tabel `transaksi`
--

CREATE TABLE `transaksi` (
  `id_transaksi` int(11) NOT NULL,
  `id_order` int(11) NOT NULL,
  `id_pelanggan` int(11) NOT NULL,
  `kode_mobil` varchar(8) NOT NULL,
  `id_driver` int(11) NOT NULL,
  `tanggal_mulai` date NOT NULL,
  `durasi` int(11) NOT NULL,
  `total` int(11) NOT NULL,
  `alamat` text NOT NULL,
  `status` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `transaksi`
--

INSERT INTO `transaksi` (`id_transaksi`, `id_order`, `id_pelanggan`, `kode_mobil`, `id_driver`, `tanggal_mulai`, `durasi`, `total`, `alamat`, `status`) VALUES
(60, 38, 1, 'crv1801', 10001, '2024-06-26', 5, 1250000, '', 'Transaksi selesai'),
(61, 39, 1, 'jzz1301', 10005, '2024-06-26', 5, 1150000, '', 'Transaksi ditolak'),
(62, 34, 2, 'crv1802', 10002, '2024-06-26', 2, 620000, '', 'Transaksi berlangsung'),
(63, 36, 2, 'day1701', 10003, '2024-06-26', 2, 550000, '', 'Transaksi berlangsung'),
(64, 37, 2, 'jzz1301', 10001, '2024-06-26', 2, 450000, '', 'Transaksi ditolak'),
(65, 40, 2, 'inv2101', 10005, '2024-06-26', 2, 500000, '', 'Transaksi ditolak'),
(66, 40, 33, 'crv1802', 10002, '2024-06-27', 5, 1550000, '', 'Transaksi berlangsung'),
(67, 41, 33, 'inv2101', 0, '2024-06-27', 5, 1000000, '', 'Transaksi berlangsung'),
(68, 39, 1, 'jzz1301', 10005, '2024-07-25', 5, 1150000, '', 'Transaksi berlangsung'),
(69, 1, 1, 'TYGT86', 10004, '0000-00-00', 10, 5700000, '', 'Transaksi ditolak'),
(70, 2, 1, 'day1701', 10002, '2024-12-26', 2, 570000, 'Bikini Bottom', 'Transaksi selesai'),
(71, 4, 1, 'crv1801', 0, '2024-12-26', 2, 400000, 'Bikini Bottom', 'Transaksi ditolak'),
(72, 4, 1, 'crv1801', 0, '2024-12-26', 2, 400000, 'Bikini Bottom', 'Transaksi ditolak'),
(73, 4, 1, 'crv1801', 0, '2024-12-26', 2, 400000, 'Bikini Bottom', 'Transaksi ditolak'),
(74, 4, 1, 'crv1801', 0, '2024-12-26', 2, 400000, 'Bikini Bottom', 'Transaksi ditolak'),
(75, 5, 1, 'inv2101', 0, '2024-12-13', 2, 400000, 'Bikini Bottom', 'Transaksi ditolak'),
(76, 5, 1, 'inv2101', 0, '0000-00-00', 2, 400000, 'Bikini Bottom', 'Transaksi ditolak'),
(77, 5, 1, 'inv2101', 0, '2024-12-26', 2, 400000, 'Bikini Bottom', 'Transaksi ditolak'),
(78, 5, 1, 'inv2101', 0, '2024-12-26', 2, 400000, 'Bikini Bottom', 'Transaksi ditolak'),
(79, 5, 1, 'inv2101', 0, '2024-12-26', 2, 400000, 'Bikini Bottom', 'Transaksi ditolak'),
(80, 5, 1, 'inv2101', 0, '2024-12-26', 2, 400000, 'Bikini Bottom', 'Transaksi ditolak'),
(81, 5, 1, 'inv2101', 0, '2024-12-26', 2, 400000, 'Bikini Bottom', 'Transaksi ditolak'),
(82, 5, 1, 'inv2101', 0, '2024-12-26', 2, 400000, 'Bikini Bottom', 'Transaksi ditolak'),
(83, 6, 1, 'day1701', 10003, '0000-00-00', 5, 1375000, 'Bikini Bottom', 'Menunggu Persetujuan');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`admin_id`);

--
-- Indexes for table `daftar_mobil`
--
ALTER TABLE `daftar_mobil`
  ADD PRIMARY KEY (`kode_mobil`);

--
-- Indexes for table `detail_mobil`
--
ALTER TABLE `detail_mobil`
  ADD PRIMARY KEY (`plat_no`),
  ADD KEY `fk_kodemobil` (`kode_mobil`);

--
-- Indexes for table `driver`
--
ALTER TABLE `driver`
  ADD PRIMARY KEY (`id_driver`);

--
-- Indexes for table `keranjang`
--
ALTER TABLE `keranjang`
  ADD PRIMARY KEY (`id_order`),
  ADD KEY `fk_pelanggan` (`id_pelanggan`),
  ADD KEY `fk_kode_mobil` (`kode_mobil`);

--
-- Indexes for table `pelanggan`
--
ALTER TABLE `pelanggan`
  ADD PRIMARY KEY (`id_pelanggan`);

--
-- Indexes for table `transaksi`
--
ALTER TABLE `transaksi`
  ADD PRIMARY KEY (`id_transaksi`),
  ADD KEY `fk_id_pelanggan` (`id_pelanggan`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `admin_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT for table `driver`
--
ALTER TABLE `driver`
  MODIFY `id_driver` int(6) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10006;
--
-- AUTO_INCREMENT for table `keranjang`
--
ALTER TABLE `keranjang`
  MODIFY `id_order` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
--
-- AUTO_INCREMENT for table `pelanggan`
--
ALTER TABLE `pelanggan`
  MODIFY `id_pelanggan` int(6) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;
--
-- AUTO_INCREMENT for table `transaksi`
--
ALTER TABLE `transaksi`
  MODIFY `id_transaksi` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=84;
--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `keranjang`
--
ALTER TABLE `keranjang`
  ADD CONSTRAINT `fk_kode_mobil` FOREIGN KEY (`kode_mobil`) REFERENCES `daftar_mobil` (`kode_mobil`),
  ADD CONSTRAINT `fk_pelanggan` FOREIGN KEY (`id_pelanggan`) REFERENCES `pelanggan` (`id_pelanggan`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ketidakleluasaan untuk tabel `transaksi`
--
ALTER TABLE `transaksi`
  ADD CONSTRAINT `fk_id_pelanggan` FOREIGN KEY (`id_pelanggan`) REFERENCES `pelanggan` (`id_pelanggan`) ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
