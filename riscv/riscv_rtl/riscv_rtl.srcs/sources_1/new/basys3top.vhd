----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 06/07/2023 05:57:43 PM
-- Design Name: 
-- Module Name: basys3top - Behavioral
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
use IEEE.std_logic_unsigned.ALL;
-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity basys3top is
    Port ( clk : in STD_LOGIC;
           seg : out STD_LOGIC_VECTOR (7 downto 0);
           ssel : out STD_LOGIC_VECTOR (3 downto 0));
end basys3top;

architecture Behavioral of basys3top is
    component cpu port ( clk : in std_logic; run : in std_logic; rst : in std_logic; rd_data : in std_logic_vector(31 downto 0); addr : out std_logic_vector(31 downto 0); wr_data : out std_logic_vector(31 downto 0); wr_flag : out std_logic_vector(3 downto 0));
    end component; 
    component seven_seg port(clk : in std_logic; data: in std_logic_vector(15 downto 0); write: in std_logic; seg: out std_logic_vector(7 downto 0); ssel: out std_logic_vector(3 downto 0));
    end component;
    component ram port ( clk    : in STD_LOGIC; addr   : in STD_LOGIC_VECTOR (31 downto 0);  w_data : in STD_LOGIC_VECTOR (31 downto 0); r_data : out STD_LOGIC_VECTOR (31 downto 0); write  : in std_logic_vector(3 downto 0) );
    end component;
    signal sseg_sel : std_logic;
begin
    sseg: seven_seg port map(clk => clk, data => x"1337", write => sseg_sel, seg => seg, ssel => ssel);

end Behavioral;
