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
    component seven_seg port(clk : in std_logic; data: in std_logic_vector(15 downto 0); seg: out std_logic_vector(7 downto 0); ssel: out std_logic_vector(3 downto 0));
    end component;
begin
    sseg: seven_seg port map(clk => clk, data => x"1337", seg => seg, ssel => ssel);

end Behavioral;
