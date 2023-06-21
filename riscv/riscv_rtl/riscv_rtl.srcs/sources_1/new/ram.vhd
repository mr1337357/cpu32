----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 06/20/2023 10:10:54 PM
-- Design Name: 
-- Module Name: ram - Behavioral
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
use ieee.numeric_std.all;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity ram is
    Port ( clk    : in STD_LOGIC;
           addr   : in STD_LOGIC_VECTOR (31 downto 0);
           w_data : in STD_LOGIC_VECTOR (31 downto 0);
           r_data : out STD_LOGIC_VECTOR (31 downto 0);
           write  : in std_logic_vector(3 downto 0) );
end ram;

architecture Behavioral of ram is
    type memory is array(65535 downto 0) of std_logic_vector(7 downto 0);
    signal mem : memory := (others => (others => '0'));
begin
    r_data( 7 downto  0) <= mem(to_integer(unsigned(addr(15 downto 0)))+ 0);
    r_data(15 downto  8) <= mem(to_integer(unsigned(addr(15 downto 0)))+ 1);
    r_data(23 downto 16) <= mem(to_integer(unsigned(addr(15 downto 0)))+ 2);
    r_data(31 downto 24) <= mem(to_integer(unsigned(addr(15 downto 0)))+ 3);
    process(clk,addr,w_data,write)
    begin
        if(rising_edge(clk))
        then
            if(write(0) = '1')
            then
                mem(to_integer(unsigned(addr(15 downto 0)))+ 0) <= w_data( 7 downto  0);
            end if;
            if(write(1) = '1')
            then
                mem(to_integer(unsigned(addr(15 downto 0)))+ 1) <= w_data(15 downto  8);
            end if;
            if(write(2) = '1')
            then
                mem(to_integer(unsigned(addr(15 downto 0)))+ 2) <= w_data(23 downto 16);
            end if;
            if(write(3) = '1')
            then
                mem(to_integer(unsigned(addr(15 downto 0)))+ 3) <= w_data(31 downto 24);
            end if;
        end if;
    end process;    
end Behavioral;
