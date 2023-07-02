----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 06/08/2023 11:02:20 AM
-- Design Name: 
-- Module Name: cpu - Behavioral
-- Project Name: 
-- Target Devices: 
-- Tool Versions: 
-- Description: 
-- 
-- Dependencies: 
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
-- 
----------------------------------------------------------------------------------


library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity cpu is
Port ( clk : in std_logic;
       run : in std_logic;
       rst : in std_logic;
       addr : out std_logic_vector(31 downto 0);
       rd_data : in std_logic_vector(31 downto 0);
       wr_data : out std_logic_vector(31 downto 0)
        );
end cpu;

architecture Behavioral of cpu is

component decoder port (
             inst : in  STD_LOGIC_VECTOR(31 downto 0);
           opcode : out STD_LOGIC_VECTOR( 6 downto 0);
               rd : out STD_LOGIC_VECTOR( 4 downto 0);
              rs1 : out STD_LOGIC_VECTOR( 4 downto 0);
              rs2 : out STD_LOGIC_VECTOR( 4 downto 0);
              imm : out STD_LOGIC_VECTOR(31 downto 0));
end component;

component registers port(
           clk : in STD_LOGIC;
           ra1 : in STD_LOGIC_VECTOR (4 downto 0);
           ra2 : in STD_LOGIC_VECTOR (4 downto 0);
           wa  : in STD_LOGIC_VECTOR (4 downto 0);
           we  : in STD_LOGIC;
           rd1 : out STD_LOGIC_VECTOR (31 downto 0);
           rd2 : out STD_LOGIC_VECTOR (31 downto 0);
           wd  : in STD_LOGIC_VECTOR (31 downto 0));
end component;

    type cpustate is ( FETCH, EXEC);
    signal  state : cpustate := FETCH;
    signal     pc : std_logic_vector(31 downto 0) := (others => '0');
    signal     ir : std_logic_vector(31 downto 0) := (others => '0');
    signal opcode : std_logic_vector( 6 downto 0);
    signal     rd : std_logic_vector( 4 downto 0);
    signal    rs1 : std_logic_vector( 4 downto 0);
    signal    rs2 : STD_LOGIC_VECTOR( 4 downto 0);
    signal    imm : STD_LOGIC_VECTOR(31 downto 0);
    signal    rd1 : STD_LOGIC_VECTOR(31 downto 0);
    signal    rd2 : STD_LOGIC_VECTOR(31 downto 0);
    signal    res : STD_LOGIC_VECTOR(31 downto 0);

begin

    reg : registers port map( clk => clk, ra1 => rs1, ra2 => rs2, wa => rd, we => '0', rd1 => rd1, rd2 => rd2, wd => res);
    dec : decoder   port map( inst => ir, opcode => opcode, rd => rd, rs1 => rs1, rs2 => rs2, imm => imm);

end Behavioral;
